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
import { fetchClimateRisk, type RawExpectedLoss } from "./climate-api-client";

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

function getStaticRawExpectedLoss(countryCode: string): RawExpectedLoss | undefined {
  const loss = staticExpectedLoss[countryCode];
  if (!loss) return undefined;
  return {
    total_annual_loss: loss.total_annual_loss,
    total_annual_loss_pct: loss.total_annual_loss_pct,
    risk_breakdown: loss.risk_breakdown,
  };
}

async function getRawExpectedLossForCountry(countryCode: string): Promise<RawExpectedLoss | undefined> {
  const countryName = getCountryName(countryCode);
  const liveData = await fetchClimateRisk(countryName);
  if (liveData) {
    return liveData;
  }
  console.log(`[Risk Calculator] Falling back to static data for ${countryCode}`);
  return getStaticRawExpectedLoss(countryCode);
}

function computePV(annualLoss: number, discountRate: number, growthRate: number, horizon: number): number {
  if (discountRate === growthRate) {
    return Math.round(annualLoss * horizon / (1 + discountRate));
  }
  const ratio = (1 + growthRate) / (1 + discountRate);
  return Math.round(annualLoss / (discountRate - growthRate) * (1 - Math.pow(ratio, horizon)));
}

function rawToExpectedLoss(
  raw: RawExpectedLoss,
  discountRate: number,
  growthRate: number,
  pvHorizon: number
): ExpectedLoss {
  const hazards = ["hurricane", "flood", "heat_stress", "drought", "extreme_precipitation"] as const;
  const breakdown: any = {};
  for (const h of hazards) {
    breakdown[h] = {
      annual_loss: raw.risk_breakdown[h].annual_loss,
      annual_loss_pct: raw.risk_breakdown[h].annual_loss_pct,
      present_value: computePV(raw.risk_breakdown[h].annual_loss, discountRate, growthRate, pvHorizon),
    };
  }
  return {
    total_annual_loss: raw.total_annual_loss,
    total_annual_loss_pct: raw.total_annual_loss_pct,
    present_value: computePV(raw.total_annual_loss, discountRate, growthRate, pvHorizon),
    discount_rate: discountRate,
    growth_rate: growthRate,
    pv_horizon: pvHorizon,
    risk_breakdown: breakdown,
  };
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

interface PVParams {
  discountRate: number;
  growthRate: number;
  pvHorizon: number;
}

const HAZARD_KEYS = ["hurricane", "flood", "heat_stress", "drought", "extreme_precipitation"] as const;

interface TierLossResult {
  total_annual_loss: number;
  total_annual_loss_pct: number;
  hazard_losses: Record<string, { annual_loss: number; annual_loss_pct: number }>;
}

function buildTierSuppliers(
  rawSuppliers: RawSupplier[],
  tier: number,
  lossMap: Map<string, RawExpectedLoss | undefined>,
  skipClimate: boolean,
  pvParams: PVParams
): {
  suppliers: Supplier[];
  tierRisk: RiskContribution;
  tierLoss: TierLossResult | undefined;
} {
  const totalCoeff = rawSuppliers.reduce((sum, s) => sum + s.coefficient, 0);

  let wClimate = 0, wSlavery = 0, wPolitical = 0, wWater = 0, wNature = 0;
  let wLoss = 0, wLossPct = 0;
  const wHazard: Record<string, { loss: number; pct: number }> = {};
  for (const h of HAZARD_KEYS) {
    wHazard[h] = { loss: 0, pct: 0 };
  }

  const suppliers: Supplier[] = rawSuppliers.map((raw) => {
    const risk = getRiskScoresForCountry(raw.country);
    const norm = totalCoeff > 0 ? raw.coefficient / totalCoeff : 0;

    wClimate += risk.climate * norm;
    wSlavery += risk.modern_slavery * norm;
    wPolitical += risk.political * norm;
    wWater += risk.water_stress * norm;
    wNature += risk.nature_loss * norm;

    const rawLoss = skipClimate ? undefined : lossMap.get(raw.country);
    let lossContribution: { annual_loss: number; present_value: number } | undefined;

    if (!skipClimate && rawLoss) {
      const annualContrib = rawLoss.total_annual_loss * norm;
      wLoss += annualContrib;
      wLossPct += rawLoss.total_annual_loss_pct * norm;
      for (const h of HAZARD_KEYS) {
        wHazard[h].loss += rawLoss.risk_breakdown[h].annual_loss * norm;
        wHazard[h].pct += rawLoss.risk_breakdown[h].annual_loss_pct * norm;
      }
      lossContribution = {
        annual_loss: round2(annualContrib),
        present_value: computePV(annualContrib, pvParams.discountRate, pvParams.growthRate, pvParams.pvHorizon),
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

  const hazardLosses: Record<string, { annual_loss: number; annual_loss_pct: number }> = {};
  for (const h of HAZARD_KEYS) {
    hazardLosses[h] = { annual_loss: round2(wHazard[h].loss), annual_loss_pct: round2(wHazard[h].pct) };
  }

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
      hazard_losses: hazardLosses,
    },
  };
}

function tierLossToExpectedLoss(tierLoss: TierLossResult, pvParams: PVParams): ExpectedLoss {
  const breakdown: any = {};
  for (const h of HAZARD_KEYS) {
    const hl = tierLoss.hazard_losses[h];
    breakdown[h] = {
      annual_loss: hl.annual_loss,
      annual_loss_pct: hl.annual_loss_pct,
      present_value: computePV(hl.annual_loss, pvParams.discountRate, pvParams.growthRate, pvParams.pvHorizon),
    };
  }
  return {
    total_annual_loss: tierLoss.total_annual_loss,
    total_annual_loss_pct: tierLoss.total_annual_loss_pct,
    present_value: computePV(tierLoss.total_annual_loss, pvParams.discountRate, pvParams.growthRate, pvParams.pvHorizon),
    discount_rate: pvParams.discountRate,
    growth_rate: pvParams.growthRate,
    pv_horizon: pvParams.pvHorizon,
    risk_breakdown: breakdown,
  };
}

export async function assessRisk(
  countryCode: string,
  sectorCode: string,
  skipClimate: boolean,
  topN: number,
  discountRate: number = 0.10,
  growthRate: number = 0.04,
  pvHorizon: number = 30
): Promise<AssessmentResponse> {
  const directRiskScores = getRiskScoresForCountry(countryCode);
  const pvParams: PVParams = { discountRate, growthRate, pvHorizon };

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

  const lossMap = new Map<string, RawExpectedLoss | undefined>();
  if (!skipClimate) {
    const BATCH_TIMEOUT_MS = 20_000;
    const countryCodes = Array.from(allCountries);

    const batchPromise = Promise.all(
      countryCodes.map(async (code) => {
        const loss = await getRawExpectedLossForCountry(code);
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
        const staticLoss = getStaticRawExpectedLoss(code);
        lossMap.set(code, staticLoss);
      }
    }
  }

  const rawDirectLoss = skipClimate ? undefined : lossMap.get(countryCode);
  const directExpectedLoss = rawDirectLoss
    ? rawToExpectedLoss(rawDirectLoss, discountRate, growthRate, pvHorizon)
    : undefined;

  const directRisk: DirectRisk = {
    ...directRiskScores,
    expected_loss: directExpectedLoss,
  };

  const t1 = buildTierSuppliers(tier1Raw, 1, lossMap, skipClimate, pvParams);
  const t2 = buildTierSuppliers(tier2Raw, 2, lossMap, skipClimate, pvParams);
  const t3 = buildTierSuppliers(tier3Raw, 3, lossMap, skipClimate, pvParams);

  const tiers = [t1, t2, t3];
  let indirectExpectedLoss: ExpectedLoss | undefined;

  if (!skipClimate) {
    const indirectTotalAnnual = round2(
      (t1.tierLoss?.total_annual_loss || 0) * TIER_WEIGHTS[0] +
      (t2.tierLoss?.total_annual_loss || 0) * TIER_WEIGHTS[1] +
      (t3.tierLoss?.total_annual_loss || 0) * TIER_WEIGHTS[2]
    );
    const indirectTotalPct = round2(
      (t1.tierLoss?.total_annual_loss_pct || 0) * TIER_WEIGHTS[0] +
      (t2.tierLoss?.total_annual_loss_pct || 0) * TIER_WEIGHTS[1] +
      (t3.tierLoss?.total_annual_loss_pct || 0) * TIER_WEIGHTS[2]
    );
    const indirectBreakdown: any = {};
    for (const h of HAZARD_KEYS) {
      const hazardAnnual = round2(
        tiers.reduce((sum, t, i) => sum + (t.tierLoss?.hazard_losses[h]?.annual_loss || 0) * TIER_WEIGHTS[i], 0)
      );
      const hazardPct = round2(
        tiers.reduce((sum, t, i) => sum + (t.tierLoss?.hazard_losses[h]?.annual_loss_pct || 0) * TIER_WEIGHTS[i], 0)
      );
      indirectBreakdown[h] = {
        annual_loss: hazardAnnual,
        annual_loss_pct: hazardPct,
        present_value: computePV(hazardAnnual, pvParams.discountRate, pvParams.growthRate, pvParams.pvHorizon),
      };
    }
    indirectExpectedLoss = {
      total_annual_loss: indirectTotalAnnual,
      total_annual_loss_pct: indirectTotalPct,
      present_value: computePV(indirectTotalAnnual, pvParams.discountRate, pvParams.growthRate, pvParams.pvHorizon),
      discount_rate: pvParams.discountRate,
      growth_rate: pvParams.growthRate,
      pv_horizon: pvParams.pvHorizon,
      risk_breakdown: indirectBreakdown,
    };
  }

  const indirectRisk: IndirectRisk = {
    climate: round2(t1.tierRisk.climate * TIER_WEIGHTS[0] + t2.tierRisk.climate * TIER_WEIGHTS[1] + t3.tierRisk.climate * TIER_WEIGHTS[2]),
    modern_slavery: round2(t1.tierRisk.modern_slavery * TIER_WEIGHTS[0] + t2.tierRisk.modern_slavery * TIER_WEIGHTS[1] + t3.tierRisk.modern_slavery * TIER_WEIGHTS[2]),
    political: round2(t1.tierRisk.political * TIER_WEIGHTS[0] + t2.tierRisk.political * TIER_WEIGHTS[1] + t3.tierRisk.political * TIER_WEIGHTS[2]),
    water_stress: round2(t1.tierRisk.water_stress * TIER_WEIGHTS[0] + t2.tierRisk.water_stress * TIER_WEIGHTS[1] + t3.tierRisk.water_stress * TIER_WEIGHTS[2]),
    nature_loss: round2(t1.tierRisk.nature_loss * TIER_WEIGHTS[0] + t2.tierRisk.nature_loss * TIER_WEIGHTS[1] + t3.tierRisk.nature_loss * TIER_WEIGHTS[2]),
    expected_loss: indirectExpectedLoss,
  };

  const totalRisk: RiskContribution = {
    climate: round2(directRiskScores.climate * 0.6 + indirectRisk.climate * 0.4),
    modern_slavery: round2(directRiskScores.modern_slavery * 0.6 + indirectRisk.modern_slavery * 0.4),
    political: round2(directRiskScores.political * 0.6 + indirectRisk.political * 0.4),
    water_stress: round2(directRiskScores.water_stress * 0.6 + indirectRisk.water_stress * 0.4),
    nature_loss: round2(directRiskScores.nature_loss * 0.6 + indirectRisk.nature_loss * 0.4),
  };

  const supplyChainTiers: TierSummary[] = tiers.map((t, i) => ({
    tier: i + 1,
    weight: TIER_WEIGHTS[i],
    supplier_count: t.suppliers.length,
    risk: t.tierRisk,
    expected_loss: t.tierLoss ? tierLossToExpectedLoss(t.tierLoss, pvParams) : undefined,
    suppliers: t.suppliers,
  }));

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
