import type {
  AssessmentResponse,
  DirectRisk,
  IndirectRisk,
  RiskContribution,
  Supplier,
  ExpectedLoss,
  CountryInfo,
  SectorInfo,
} from "@shared/schema";
import countriesData from "./data/countries.json";
import sectorsData from "./data/sectors.json";
import riskScoresData from "./data/risk-scores.json";
import expectedLossData from "./data/expected-loss.json";
import ioCoefficientsData from "./data/io-coefficients.json";
import { fetchClimateRisk } from "./climate-api-client";

const countries: CountryInfo[] = countriesData;
const sectors: SectorInfo[] = sectorsData;
const riskScores: Record<string, Record<string, number>> = riskScoresData;
const staticExpectedLoss: Record<string, any> = expectedLossData;
const ioCoefficients: Record<string, any> = ioCoefficientsData;

export function getCountries(): CountryInfo[] {
  return countries;
}

export function getSectors(): SectorInfo[] {
  return sectors;
}

export function getCountryName(code: string): string {
  const country = countries.find((c) => c.code === code);
  return country ? country.name : code;
}

export function getSectorName(code: string): string {
  const sector = sectors.find((s) => s.code === code);
  return sector ? sector.name : code;
}

export function isValidCountry(code: string): boolean {
  return countries.some((c) => c.code === code);
}

export function isValidSector(code: string): boolean {
  return sectors.some((s) => s.code === code);
}

function getRiskScoresForCountry(countryCode: string): RiskContribution {
  const scores = riskScores[countryCode];
  if (scores) {
    return {
      climate: scores.climate,
      modern_slavery: scores.modern_slavery,
      political: scores.political,
      water_stress: scores.water_stress,
      nature_loss: scores.nature_loss,
    };
  }
  return { climate: 2.5, modern_slavery: 2.5, political: 2.5, water_stress: 2.5, nature_loss: 2.5 };
}

function getStaticExpectedLoss(countryCode: string): ExpectedLoss | undefined {
  const loss = staticExpectedLoss[countryCode];
  if (!loss) return undefined;
  return {
    total_annual_loss: loss.total_annual_loss,
    total_annual_loss_pct: loss.total_annual_loss_pct,
    present_value_30yr: loss.present_value_30yr,
    risk_breakdown: loss.risk_breakdown,
  };
}

async function getExpectedLossForCountry(countryCode: string): Promise<ExpectedLoss | undefined> {
  const countryName = getCountryName(countryCode);
  const liveData = await fetchClimateRisk(countryName);
  if (liveData) {
    return liveData;
  }
  console.log(`[Risk Calculator] Falling back to static data for ${countryCode}`);
  return getStaticExpectedLoss(countryCode);
}

interface RawSupplier {
  country: string;
  sector: string;
  coefficient: number;
}

function getSuppliers(countryCode: string, sectorCode: string, topN: number): RawSupplier[] {
  const countryData = ioCoefficients[countryCode];
  let suppliers: RawSupplier[];

  if (countryData && countryData[sectorCode]) {
    suppliers = countryData[sectorCode];
  } else if (countryData) {
    const firstSector = Object.keys(countryData)[0];
    if (firstSector) {
      suppliers = countryData[firstSector];
    } else {
      suppliers = ioCoefficients["_default"];
    }
  } else {
    suppliers = ioCoefficients["_default"];
  }

  return suppliers.slice(0, topN);
}

export async function assessRisk(
  countryCode: string,
  sectorCode: string,
  skipClimate: boolean,
  topN: number
): Promise<AssessmentResponse> {
  const directRiskScores = getRiskScoresForCountry(countryCode);
  const rawSuppliers = getSuppliers(countryCode, sectorCode, topN);

  let directExpectedLoss: ExpectedLoss | undefined;
  const supplierLossMap = new Map<string, ExpectedLoss | undefined>();

  if (!skipClimate) {
    const uniqueCountries = new Set<string>([countryCode]);
    for (const s of rawSuppliers) {
      uniqueCountries.add(s.country);
    }

    const lossResults = await Promise.all(
      Array.from(uniqueCountries).map(async (code) => {
        const loss = await getExpectedLossForCountry(code);
        return { code, loss };
      })
    );

    for (const { code, loss } of lossResults) {
      supplierLossMap.set(code, loss);
    }
    directExpectedLoss = supplierLossMap.get(countryCode);
  }

  const directRisk: DirectRisk = {
    ...directRiskScores,
    expected_loss: skipClimate ? undefined : directExpectedLoss,
  };

  const totalCoefficient = rawSuppliers.reduce((sum, s) => sum + s.coefficient, 0);

  let indirectClimate = 0;
  let indirectSlavery = 0;
  let indirectPolitical = 0;
  let indirectWater = 0;
  let indirectNature = 0;
  let indirectExpectedLoss = 0;
  let indirectExpectedLossPct = 0;

  const enrichedSuppliers: Supplier[] = rawSuppliers.map((raw) => {
    const supplierRisk = getRiskScoresForCountry(raw.country);
    const normalizedCoeff = totalCoefficient > 0 ? raw.coefficient / totalCoefficient : 0;

    indirectClimate += supplierRisk.climate * normalizedCoeff;
    indirectSlavery += supplierRisk.modern_slavery * normalizedCoeff;
    indirectPolitical += supplierRisk.political * normalizedCoeff;
    indirectWater += supplierRisk.water_stress * normalizedCoeff;
    indirectNature += supplierRisk.nature_loss * normalizedCoeff;

    const supplierLoss = skipClimate ? undefined : supplierLossMap.get(raw.country);
    let lossContribution: { annual_loss: number; present_value_30yr: number } | undefined;

    if (!skipClimate && supplierLoss) {
      const annualLossContrib = supplierLoss.total_annual_loss * normalizedCoeff;
      const pvContrib = supplierLoss.present_value_30yr * normalizedCoeff;
      indirectExpectedLoss += annualLossContrib;
      indirectExpectedLossPct += supplierLoss.total_annual_loss_pct * normalizedCoeff;
      lossContribution = {
        annual_loss: Math.round(annualLossContrib * 100) / 100,
        present_value_30yr: Math.round(pvContrib),
      };
    }

    return {
      country: raw.country,
      sector: raw.sector,
      coefficient: raw.coefficient,
      country_name: getCountryName(raw.country),
      sector_name: getSectorName(raw.sector),
      direct_risk: supplierRisk,
      risk_contribution: {
        climate: Math.round(supplierRisk.climate * normalizedCoeff * 10000) / 10000,
        modern_slavery: Math.round(supplierRisk.modern_slavery * normalizedCoeff * 10000) / 10000,
        political: Math.round(supplierRisk.political * normalizedCoeff * 10000) / 10000,
        water_stress: Math.round(supplierRisk.water_stress * normalizedCoeff * 10000) / 10000,
        nature_loss: Math.round(supplierRisk.nature_loss * normalizedCoeff * 10000) / 10000,
      },
      expected_loss_contribution: lossContribution,
    };
  });

  const indirectRisk: IndirectRisk = {
    climate: Math.round(indirectClimate * 100) / 100,
    modern_slavery: Math.round(indirectSlavery * 100) / 100,
    political: Math.round(indirectPolitical * 100) / 100,
    water_stress: Math.round(indirectWater * 100) / 100,
    nature_loss: Math.round(indirectNature * 100) / 100,
    expected_loss: skipClimate
      ? undefined
      : {
          total_annual_loss: Math.round(indirectExpectedLoss * 100) / 100,
          total_annual_loss_pct: Math.round(indirectExpectedLossPct * 100) / 100,
        },
  };

  const totalRisk: RiskContribution = {
    climate: Math.round(((directRiskScores.climate * 0.6 + indirectRisk.climate * 0.4) * 100)) / 100,
    modern_slavery: Math.round(((directRiskScores.modern_slavery * 0.6 + indirectRisk.modern_slavery * 0.4) * 100)) / 100,
    political: Math.round(((directRiskScores.political * 0.6 + indirectRisk.political * 0.4) * 100)) / 100,
    water_stress: Math.round(((directRiskScores.water_stress * 0.6 + indirectRisk.water_stress * 0.4) * 100)) / 100,
    nature_loss: Math.round(((directRiskScores.nature_loss * 0.6 + indirectRisk.nature_loss * 0.4) * 100)) / 100,
  };

  return {
    country: countryCode,
    country_name: getCountryName(countryCode),
    sector: sectorCode,
    sector_name: getSectorName(sectorCode),
    direct_risk: directRisk,
    indirect_risk: indirectRisk,
    total_risk: totalRisk,
    top_suppliers: enrichedSuppliers,
  };
}
