import type {
  AssessmentResponse,
  DirectRisk,
  IndirectRisk,
  RiskContribution,
  Supplier,
  ExpectedLoss,
  TierSummary,
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

const TIER_WEIGHTS = [0.50, 0.35, 0.15];

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

function getRawSuppliers(countryCode: string, sectorCode: string, topN: number): RawSupplier[] {
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

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}

function round4(n: number): number {
  return Math.round(n * 10000) / 10000;
}

function buildTierSuppliers(
  rawSuppliers: RawSupplier[],
  tier: number,
  lossMap: Map<string, ExpectedLoss | undefined>,
  skipClimate: boolean
): {
  suppliers: Supplier[];
  tierRisk: RiskContribution;
  tierLoss: { total_annual_loss: number; total_annual_loss_pct: number } | undefined;
} {
  const totalCoeff = rawSuppliers.reduce((sum, s) => sum + s.coefficient, 0);

  let wClimate = 0, wSlavery = 0, wPolitical = 0, wWater = 0, wNature = 0;
  let wLoss = 0, wLossPct = 0;

  const suppliers: Supplier[] = rawSuppliers.map((raw) => {
    const risk = getRiskScoresForCountry(raw.country);
    const norm = totalCoeff > 0 ? raw.coefficient / totalCoeff : 0;

    wClimate += risk.climate * norm;
    wSlavery += risk.modern_slavery * norm;
    wPolitical += risk.political * norm;
    wWater += risk.water_stress * norm;
    wNature += risk.nature_loss * norm;

    const loss = skipClimate ? undefined : lossMap.get(raw.country);
    let lossContribution: { annual_loss: number; present_value_30yr: number } | undefined;

    if (!skipClimate && loss) {
      const annualContrib = loss.total_annual_loss * norm;
      const pvContrib = loss.present_value_30yr * norm;
      wLoss += annualContrib;
      wLossPct += loss.total_annual_loss_pct * norm;
      lossContribution = {
        annual_loss: round2(annualContrib),
        present_value_30yr: Math.round(pvContrib),
      };
    }

    return {
      country: raw.country,
      sector: raw.sector,
      coefficient: raw.coefficient,
      country_name: getCountryName(raw.country),
      sector_name: getSectorName(raw.sector),
      tier,
      direct_risk: risk,
      risk_contribution: {
        climate: round4(risk.climate * norm),
        modern_slavery: round4(risk.modern_slavery * norm),
        political: round4(risk.political * norm),
        water_stress: round4(risk.water_stress * norm),
        nature_loss: round4(risk.nature_loss * norm),
      },
      expected_loss_contribution: lossContribution,
    };
  });

  return {
    suppliers,
    tierRisk: {
      climate: round2(wClimate),
      modern_slavery: round2(wSlavery),
      political: round2(wPolitical),
      water_stress: round2(wWater),
      nature_loss: round2(wNature),
    },
    tierLoss: skipClimate ? undefined : {
      total_annual_loss: round2(wLoss),
      total_annual_loss_pct: round2(wLossPct),
    },
  };
}

export async function assessRisk(
  countryCode: string,
  sectorCode: string,
  skipClimate: boolean,
  topN: number
): Promise<AssessmentResponse> {
  const directRiskScores = getRiskScoresForCountry(countryCode);

  const tier1Raw = getRawSuppliers(countryCode, sectorCode, topN);

  const tier2RawByParent: RawSupplier[][] = [];
  for (const t1 of tier1Raw) {
    tier2RawByParent.push(getRawSuppliers(t1.country, t1.sector, topN));
  }
  const tier2Raw = deduplicateSuppliers(tier2RawByParent.flat());

  const tier3RawByParent: RawSupplier[][] = [];
  for (const t2 of tier2Raw) {
    tier3RawByParent.push(getRawSuppliers(t2.country, t2.sector, Math.min(topN, 5)));
  }
  const tier3Raw = deduplicateSuppliers(tier3RawByParent.flat());

  const allCountries = new Set<string>([countryCode]);
  for (const s of [...tier1Raw, ...tier2Raw, ...tier3Raw]) {
    allCountries.add(s.country);
  }

  const lossMap = new Map<string, ExpectedLoss | undefined>();
  if (!skipClimate) {
    const BATCH_TIMEOUT_MS = 20_000;
    const countryCodes = Array.from(allCountries);

    const batchPromise = Promise.all(
      countryCodes.map(async (code) => {
        const loss = await getExpectedLossForCountry(code);
        return { code, loss };
      })
    );

    const timeoutPromise = new Promise<null>((resolve) =>
      setTimeout(() => {
        console.log(`[Risk Calculator] Climate batch timeout (${BATCH_TIMEOUT_MS}ms) — using fallback data for remaining countries`);
        resolve(null);
      }, BATCH_TIMEOUT_MS)
    );

    const results = await Promise.race([batchPromise, timeoutPromise]);

    if (results) {
      for (const { code, loss } of results) {
        lossMap.set(code, loss);
      }
    }

    for (const code of countryCodes) {
      if (!lossMap.has(code)) {
        const staticLoss = getStaticExpectedLoss(code);
        lossMap.set(code, staticLoss);
      }
    }
  }

  const directExpectedLoss = skipClimate ? undefined : lossMap.get(countryCode);
  const directRisk: DirectRisk = {
    ...directRiskScores,
    expected_loss: directExpectedLoss,
  };

  const t1 = buildTierSuppliers(tier1Raw, 1, lossMap, skipClimate);
  const t2 = buildTierSuppliers(tier2Raw, 2, lossMap, skipClimate);
  const t3 = buildTierSuppliers(tier3Raw, 3, lossMap, skipClimate);

  const indirectRisk: IndirectRisk = {
    climate: round2(t1.tierRisk.climate * TIER_WEIGHTS[0] + t2.tierRisk.climate * TIER_WEIGHTS[1] + t3.tierRisk.climate * TIER_WEIGHTS[2]),
    modern_slavery: round2(t1.tierRisk.modern_slavery * TIER_WEIGHTS[0] + t2.tierRisk.modern_slavery * TIER_WEIGHTS[1] + t3.tierRisk.modern_slavery * TIER_WEIGHTS[2]),
    political: round2(t1.tierRisk.political * TIER_WEIGHTS[0] + t2.tierRisk.political * TIER_WEIGHTS[1] + t3.tierRisk.political * TIER_WEIGHTS[2]),
    water_stress: round2(t1.tierRisk.water_stress * TIER_WEIGHTS[0] + t2.tierRisk.water_stress * TIER_WEIGHTS[1] + t3.tierRisk.water_stress * TIER_WEIGHTS[2]),
    nature_loss: round2(t1.tierRisk.nature_loss * TIER_WEIGHTS[0] + t2.tierRisk.nature_loss * TIER_WEIGHTS[1] + t3.tierRisk.nature_loss * TIER_WEIGHTS[2]),
    expected_loss: skipClimate ? undefined : {
      total_annual_loss: round2(
        (t1.tierLoss?.total_annual_loss || 0) * TIER_WEIGHTS[0] +
        (t2.tierLoss?.total_annual_loss || 0) * TIER_WEIGHTS[1] +
        (t3.tierLoss?.total_annual_loss || 0) * TIER_WEIGHTS[2]
      ),
      total_annual_loss_pct: round2(
        (t1.tierLoss?.total_annual_loss_pct || 0) * TIER_WEIGHTS[0] +
        (t2.tierLoss?.total_annual_loss_pct || 0) * TIER_WEIGHTS[1] +
        (t3.tierLoss?.total_annual_loss_pct || 0) * TIER_WEIGHTS[2]
      ),
    },
  };

  const totalRisk: RiskContribution = {
    climate: round2(directRiskScores.climate * 0.6 + indirectRisk.climate * 0.4),
    modern_slavery: round2(directRiskScores.modern_slavery * 0.6 + indirectRisk.modern_slavery * 0.4),
    political: round2(directRiskScores.political * 0.6 + indirectRisk.political * 0.4),
    water_stress: round2(directRiskScores.water_stress * 0.6 + indirectRisk.water_stress * 0.4),
    nature_loss: round2(directRiskScores.nature_loss * 0.6 + indirectRisk.nature_loss * 0.4),
  };

  const supplyChainTiers: TierSummary[] = [
    { tier: 1, weight: TIER_WEIGHTS[0], supplier_count: t1.suppliers.length, risk: t1.tierRisk, expected_loss: t1.tierLoss, suppliers: t1.suppliers },
    { tier: 2, weight: TIER_WEIGHTS[1], supplier_count: t2.suppliers.length, risk: t2.tierRisk, expected_loss: t2.tierLoss, suppliers: t2.suppliers },
    { tier: 3, weight: TIER_WEIGHTS[2], supplier_count: t3.suppliers.length, risk: t3.tierRisk, expected_loss: t3.tierLoss, suppliers: t3.suppliers },
  ];

  const allSuppliers = [...t1.suppliers, ...t2.suppliers, ...t3.suppliers];

  return {
    country: countryCode,
    country_name: getCountryName(countryCode),
    sector: sectorCode,
    sector_name: getSectorName(sectorCode),
    direct_risk: directRisk,
    indirect_risk: indirectRisk,
    total_risk: totalRisk,
    supply_chain_tiers: supplyChainTiers,
    top_suppliers: allSuppliers,
  };
}

function deduplicateSuppliers(suppliers: RawSupplier[]): RawSupplier[] {
  const map = new Map<string, RawSupplier>();
  for (const s of suppliers) {
    const key = `${s.country}:${s.sector}`;
    const existing = map.get(key);
    if (existing) {
      existing.coefficient = Math.max(existing.coefficient, s.coefficient);
    } else {
      map.set(key, { ...s });
    }
  }
  return Array.from(map.values())
    .sort((a, b) => b.coefficient - a.coefficient)
    .slice(0, 20);
}
