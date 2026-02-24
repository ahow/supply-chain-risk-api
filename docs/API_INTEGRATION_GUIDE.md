# Supply Chain Risk Assessment API - Integration Guide

## Base URL

```
https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com
```

## Overview

This API quantifies multi-dimensional supply chain risk exposure for any country-sector combination. It integrates 5 risk dimensions with OECD Input-Output economic modeling to assess both direct operational risk and indirect (upstream supply chain) risk.

The 5 risk dimensions are:
- **Climate** - physical climate hazard exposure
- **Modern Slavery** - forced labour and trafficking risk
- **Political Instability** - governance and political risk
- **Water Stress** - water scarcity and stress exposure
- **Nature Loss** - biodiversity and ecosystem degradation risk

All risk scores are on a scale of **0 to 5**, where 0 = lowest risk and 5 = highest risk.

## Authentication

No authentication is required. The API is publicly accessible.

## Integration with ISIN-based Systems

The API uses **ISO-3166 country codes** (e.g., USA, GBR, CHN) and **ISIC Rev.4 sector codes** (e.g., B06, C20) as identifiers. To integrate with a system that uses ISINs as the primary company identifier, the consuming application should:

1. Extract the **country of domicile** from the ISIN (first 2 characters map to ISO-2, which should be converted to ISO-3)
2. Map the company's **primary business activity** to an ISIC sector code (e.g., using GICS, ICB, or NACE classification crosswalks)
3. Call the `/api/assess` endpoint with those two parameters

**ISIN country prefix to ISO-3 mapping examples:**

| ISIN Prefix | Country      | ISO-3 Code |
|-------------|-------------|------------|
| US          | United States | USA        |
| GB          | United Kingdom | GBR      |
| DE          | Germany      | DEU        |
| JP          | Japan        | JPN        |
| FR          | France       | FRA        |
| CN          | China        | CHN        |
| AU          | Australia    | AUS        |
| BR          | Brazil       | BRA        |
| IN          | India        | IND        |
| CH          | Switzerland  | CHE        |

For a full list of supported countries, call `GET /api/countries`.

---

## Endpoints

### 1. Health Check

```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "4.0.0",
  "countries": 85,
  "sectors": 52
}
```

---

### 2. List Countries

```
GET /api/countries
```

Returns all 85 supported countries with ISO-3 codes and regions.

**Response:**
```json
[
  { "code": "AUS", "name": "Australia", "region": "Asia-Pacific" },
  { "code": "GBR", "name": "United Kingdom", "region": "Europe" },
  { "code": "USA", "name": "United States", "region": "Americas" }
]
```

---

### 3. List Sectors

```
GET /api/sectors
```

Returns all 52 supported ISIC Rev.4 sectors with categories.

**Response:**
```json
[
  { "code": "A01", "name": "Crop and animal production", "category": "Agriculture" },
  { "code": "B06", "name": "Mining and quarrying", "category": "Mining" },
  { "code": "C20", "name": "Chemicals and chemical products", "category": "Manufacturing" },
  { "code": "K64", "name": "Financial service activities", "category": "Finance" }
]
```

**Full sector list:**

| Code | Name | Category |
|------|------|----------|
| A01 | Crop and animal production | Agriculture |
| A02 | Forestry and logging | Agriculture |
| A03 | Fishing and aquaculture | Agriculture |
| B05 | Mining of coal and lignite | Mining |
| B06 | Mining and quarrying | Mining |
| B07-B08 | Mining of metal ores and other mining | Mining |
| B09 | Mining support service activities | Mining |
| C10-C12 | Food products, beverages and tobacco | Manufacturing |
| C13-C15 | Textiles, wearing apparel and leather | Manufacturing |
| C16 | Wood and products of wood | Manufacturing |
| C17-C18 | Paper products and printing | Manufacturing |
| C19 | Coke and refined petroleum products | Manufacturing |
| C20 | Chemicals and chemical products | Manufacturing |
| C21 | Pharmaceuticals | Manufacturing |
| C22 | Rubber and plastics products | Manufacturing |
| C23 | Other non-metallic mineral products | Manufacturing |
| C24 | Basic metals | Manufacturing |
| C25 | Fabricated metal products | Manufacturing |
| C26 | Computer, electronic and optical products | Manufacturing |
| C27 | Electrical equipment | Manufacturing |
| C28 | Machinery and equipment | Manufacturing |
| C29 | Motor vehicles and trailers | Manufacturing |
| C30 | Other transport equipment | Manufacturing |
| C31-C33 | Furniture and other manufacturing | Manufacturing |
| D35 | Electricity, gas, steam and air conditioning | Utilities |
| E36 | Water collection and treatment | Utilities |
| E37-E39 | Sewerage and waste management | Utilities |
| F | Construction | Construction |
| G45 | Wholesale and retail trade of motor vehicles | Trade |
| G46 | Wholesale trade | Trade |
| G47 | Retail trade | Trade |
| H49 | Land transport and pipelines | Transport |
| H50 | Water transport | Transport |
| H51 | Air transport | Transport |
| H52 | Warehousing and support for transportation | Transport |
| H53 | Postal and courier activities | Transport |
| I | Accommodation and food service | Services |
| J58-J60 | Publishing, audiovisual and broadcasting | ICT |
| J61 | Telecommunications | ICT |
| J62-J63 | IT and other information services | ICT |
| K64 | Financial service activities | Finance |
| K65 | Insurance and pension funding | Finance |
| K66 | Auxiliary financial services | Finance |
| L68 | Real estate activities | Real Estate |
| M | Professional, scientific and technical activities | Professional |
| N | Administrative and support services | Professional |
| O | Public administration and defence | Public |
| P | Education | Public |
| Q | Human health and social work | Public |
| R | Arts, entertainment and recreation | Services |
| S-U | Other service activities | Services |

---

### 4. Risk Assessment (Primary Endpoint)

```
GET /api/assess?country={ISO3_CODE}&sector={ISIC_CODE}
```

**Parameters:**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| country   | string | Yes      | ISO-3166 alpha-3 country code (e.g., USA, GBR, CHN) |
| sector    | string | Yes      | ISIC Rev.4 sector code (e.g., B06, C20, K64) |

**Example Request:**
```
GET /api/assess?country=USA&sector=B06
```

**Response Structure:**

> **Note:** Climate expected loss data is now sourced **live** from the Climate Risk API V6 (Probabilistic Model), which uses real scientific datasets (NOAA IBTrACS, WRI Aqueduct, HadEX3). If the Climate API is temporarily unavailable, the system falls back to pre-computed static values. Results are cached for 1 hour per country to optimize response times.

```json
{
  "country": "USA",
  "country_name": "United States",
  "sector": "B06",
  "sector_name": "Mining and quarrying",

  "direct_risk": {
    "climate": 2.74,
    "modern_slavery": 2.22,
    "political": 2.18,
    "water_stress": 2.76,
    "nature_loss": 2.61,
    "expected_loss": {
      "total_annual_loss": 100886.20,
      "total_annual_loss_pct": 10.09,
      "present_value_30yr": 1977414,
      "risk_breakdown": {
        "hurricane": { "annual_loss": 0, "annual_loss_pct": 0 },
        "flood": { "annual_loss": 97205.72, "annual_loss_pct": 9.72 },
        "heat_stress": { "annual_loss": 2356.16, "annual_loss_pct": 0.24 },
        "drought": { "annual_loss": 1324.32, "annual_loss_pct": 0.13 },
        "extreme_precipitation": { "annual_loss": 0, "annual_loss_pct": 0 }
      }
    }
  },

  "indirect_risk": {
    "climate": 2.64,
    "modern_slavery": 2.06,
    "political": 1.99,
    "water_stress": 2.54,
    "nature_loss": 2.55,
    "expected_loss": {
      "total_annual_loss": 92758.11,
      "total_annual_loss_pct": 9.28
    }
  },

  "total_risk": {
    "climate": 2.70,
    "modern_slavery": 2.16,
    "political": 2.10,
    "water_stress": 2.67,
    "nature_loss": 2.59
  },

  "top_suppliers": [
    {
      "country": "USA",
      "sector": "M",
      "coefficient": 0.0475,
      "country_name": "United States",
      "sector_name": "Professional, scientific and technical activities",
      "direct_risk": {
        "climate": 2.74,
        "modern_slavery": 2.22,
        "political": 2.18,
        "water_stress": 2.76,
        "nature_loss": 2.61
      },
      "risk_contribution": {
        "climate": 0.7647,
        "modern_slavery": 0.6196,
        "political": 0.6084,
        "water_stress": 0.7703,
        "nature_loss": 0.7284
      },
      "expected_loss_contribution": {
        "annual_loss": 28155.67,
        "present_value_30yr": 432579
      }
    }
  ]
}
```

**Response Field Definitions:**

| Field | Description |
|-------|-------------|
| `direct_risk` | Risk scores for the country where the company operates directly |
| `direct_risk.expected_loss` | Financial loss estimates from physical hazards (USD millions) |
| `direct_risk.expected_loss.total_annual_loss` | Total expected annual loss in USD millions |
| `direct_risk.expected_loss.total_annual_loss_pct` | Annual loss as percentage of GDP |
| `direct_risk.expected_loss.present_value_30yr` | Present value of losses over 30 years (USD millions) |
| `direct_risk.expected_loss.risk_breakdown` | Loss decomposed by hazard type |
| `indirect_risk` | Weighted average risk from upstream supply chain (I-O model) |
| `indirect_risk.expected_loss` | Aggregated expected loss from all upstream suppliers |
| `total_risk` | Blended score combining direct and indirect risk |
| `top_suppliers` | Top 5 upstream sector-country pairs by I-O coefficient |
| `top_suppliers[].coefficient` | OECD I-O coefficient (share of inputs from this supplier) |
| `top_suppliers[].risk_contribution` | Absolute risk contributed by this supplier to indirect risk |
| `top_suppliers[].expected_loss_contribution` | Financial loss attributed to this supplier relationship |

---

## Integration Examples

### Python

```python
import requests

BASE_URL = "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com"

def get_risk_assessment(country_iso3: str, sector_isic: str) -> dict:
    response = requests.get(
        f"{BASE_URL}/api/assess",
        params={"country": country_iso3, "sector": sector_isic}
    )
    response.raise_for_status()
    return response.json()

# Example: Assess mining risk in the USA
result = get_risk_assessment("USA", "B06")
print(f"Total climate risk: {result['total_risk']['climate']}")
print(f"Annual expected loss: ${result['direct_risk']['expected_loss']['total_annual_loss']:,.0f}M")
```

### JavaScript / TypeScript

```javascript
const BASE_URL = "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com";

async function getRiskAssessment(country, sector) {
  const response = await fetch(
    `${BASE_URL}/api/assess?country=${country}&sector=${sector}`
  );
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

// Example: Assess pharmaceutical risk in India
const result = await getRiskAssessment("IND", "C21");
console.log("Total risk:", result.total_risk);
console.log("Top supplier:", result.top_suppliers[0].country_name);
```

### ISIN-to-Assessment Workflow (Python)

```python
import pycountry

# ISIN country prefix to ISO-3 mapping
def isin_to_iso3(isin: str) -> str:
    iso2 = isin[:2]
    country = pycountry.countries.get(alpha_2=iso2)
    return country.alpha_3 if country else None

# Example: Apple Inc. (ISIN: US0378331005)
isin = "US0378331005"
country_code = isin_to_iso3(isin)  # Returns "USA"
sector_code = "C26"  # Computer, electronic and optical products

assessment = get_risk_assessment(country_code, sector_code)
```

---

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 400 | Invalid country or sector code |
| 404 | Endpoint not found |
| 500 | Server error |

**Error response format:**
```json
{
  "error": "Invalid country code: XYZ"
}
```

---

## Climate Risk Data Source

The `expected_loss` fields in the response are sourced **live** from the [Climate Risk API V6 (Probabilistic Model)](https://climate-risk-api-v6-prob-be68437e49be.herokuapp.com), which calculates Expected Annual Loss (EAL) per $1M of exposure using real scientific datasets:

| Data Source | Coverage | Description |
|-------------|----------|-------------|
| NOAA IBTrACS | 131,076 hurricane records (2004–2024) | Global tropical cyclone basin data |
| WRI Aqueduct | 7,473 flood grid points, 7 return periods | Global flood risk modeling |
| HadEX3 | Temperature + precipitation extremes | Global land, 2.5° grid (GEV/Gamma distributions) |

**How it works:**
1. When a risk assessment is requested, the supply chain API calls the Climate Risk API's country endpoint with `asset_value = $1,000,000`
2. The Climate API evaluates a 9-point weighted grid across the country (center 25%, cardinals 10% each, diagonals 9% each)
3. Results are cached for 1 hour per country to reduce response times on subsequent requests
4. If the Climate API is temporarily unavailable (e.g., cold start, maintenance), the system falls back to pre-computed static values

**Response time impact:** The first request for a given country takes 20–30 seconds (Climate API processing time). Subsequent requests within the 1-hour cache window return in <100ms.

---

## Rate Limits

No rate limits are currently enforced. Note that the first request for each country may take 20–30 seconds due to the live Climate Risk API call. For bulk assessments, results are cached for 1 hour, so subsequent requests for the same country will be fast.

## Availability

The API runs on a Heroku Basic dyno and is available 24/7 with no scheduled downtime or sleep periods. The Climate Risk API V6 also runs on Heroku (Standard-2X dyno) and is available 24/7.

## Coverage

- **85 countries** across all major economic regions
- **52 sectors** based on ISIC Rev.4 classification
- **5 risk dimensions** per country
- **OECD I-O coefficients** for upstream supply chain modeling
- **Live climate data** from NOAA, WRI Aqueduct, and HadEX3 via Climate Risk API V6
