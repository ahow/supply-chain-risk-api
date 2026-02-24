import type { ExpectedLoss } from "@shared/schema";

const CLIMATE_API_BASE = "https://climate-risk-api-v6-prob-be68437e49be.herokuapp.com";
const ASSET_VALUE = 1_000_000;
const CACHE_TTL_MS = 60 * 60 * 1000;
const REQUEST_TIMEOUT_MS = 15_000;

interface ClimateApiResponse {
  expected_annual_loss: number;
  expected_annual_loss_pct: number;
  present_value_30yr: number;
  country: string;
  country_name: string;
  risk_breakdown: {
    hurricane: { annual_loss: number; annual_loss_pct: number };
    flood: { annual_loss: number; annual_loss_pct: number };
    heat_stress: { annual_loss: number; annual_loss_pct: number };
    drought: { annual_loss: number; annual_loss_pct: number };
    extreme_precipitation: { annual_loss: number; annual_loss_pct: number };
  };
}

interface CacheEntry {
  data: ExpectedLoss;
  timestamp: number;
}

const cache = new Map<string, CacheEntry>();

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}

function mapResponseToExpectedLoss(response: ClimateApiResponse): ExpectedLoss {
  return {
    total_annual_loss: round2(response.expected_annual_loss),
    total_annual_loss_pct: round2(response.expected_annual_loss_pct),
    present_value_30yr: Math.round(response.present_value_30yr),
    risk_breakdown: {
      hurricane: {
        annual_loss: round2(response.risk_breakdown.hurricane.annual_loss),
        annual_loss_pct: round2(response.risk_breakdown.hurricane.annual_loss_pct),
      },
      flood: {
        annual_loss: round2(response.risk_breakdown.flood.annual_loss),
        annual_loss_pct: round2(response.risk_breakdown.flood.annual_loss_pct),
      },
      heat_stress: {
        annual_loss: round2(response.risk_breakdown.heat_stress.annual_loss),
        annual_loss_pct: round2(response.risk_breakdown.heat_stress.annual_loss_pct),
      },
      drought: {
        annual_loss: round2(response.risk_breakdown.drought.annual_loss),
        annual_loss_pct: round2(response.risk_breakdown.drought.annual_loss_pct),
      },
      extreme_precipitation: {
        annual_loss: round2(response.risk_breakdown.extreme_precipitation.annual_loss),
        annual_loss_pct: round2(response.risk_breakdown.extreme_precipitation.annual_loss_pct),
      },
    },
  };
}

export async function fetchClimateRisk(countryName: string): Promise<ExpectedLoss | null> {
  const cacheKey = countryName.toLowerCase();
  const cached = cache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    console.log(`[Climate API] Cache hit for ${countryName}`);
    return cached.data;
  }

  try {
    console.log(`[Climate API] Fetching live data for ${countryName}...`);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    const response = await fetch(`${CLIMATE_API_BASE}/assess/country`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        country: countryName,
        asset_value: ASSET_VALUE,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      console.error(`[Climate API] Error for ${countryName}: HTTP ${response.status}`);
      return null;
    }

    const data: ClimateApiResponse = await response.json();
    const expectedLoss = mapResponseToExpectedLoss(data);

    cache.set(cacheKey, { data: expectedLoss, timestamp: Date.now() });
    console.log(`[Climate API] Success for ${countryName}: EAL $${data.expected_annual_loss.toLocaleString()}`);

    return expectedLoss;
  } catch (error: any) {
    if (error.name === "AbortError") {
      console.error(`[Climate API] Timeout for ${countryName} (>${REQUEST_TIMEOUT_MS}ms)`);
    } else {
      console.error(`[Climate API] Failed for ${countryName}:`, error.message);
    }
    return null;
  }
}

export function clearClimateCache(): void {
  cache.clear();
}

export function getClimateCacheStats(): { size: number; countries: string[] } {
  return {
    size: cache.size,
    countries: Array.from(cache.keys()),
  };
}
