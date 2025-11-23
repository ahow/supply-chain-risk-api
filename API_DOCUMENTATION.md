# Supply Chain Risk Exposure Assessment API

Comprehensive API for assessing supply chain risk exposure using Input-Output (I-O) economic models and real-world risk data.

## Base URL

```
https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com
```

## Authentication

All API endpoints (except `/` and `/api/health`) require API key authentication via the `X-API-Key` header.

```bash
curl -H "X-API-Key: YOUR_API_KEY" https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=USA&sector=C10T12&model=oecd
```

**API Key:** `zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM`

---

## Core Concepts

### Risk Types

The API assesses **5 independent risk types**:

1. **Climate Risk** - Physical climate risks (floods, droughts, storms, heat stress)
2. **Modern Slavery Risk** - Labor exploitation and forced labor prevalence
3. **Political Risk** - Governance instability and regulatory exposure
4. **Water Stress Risk** - Water scarcity and quality issues
5. **Nature Loss Risk** - Biodiversity loss and ecosystem degradation

### Risk Scores

- **Scale:** 0-10 (higher = more risk)
- **Direct Risk:** Inherent risk of the target country-sector (70% country + 30% sector)
- **Indirect Risk:** Weighted supplier risk across 3 tiers using I-O coefficients
- **Total Risk:** Combined exposure (60% direct + 40% indirect)

### Expected Loss

Financial impact estimates from physical climate hazards (per $1M asset value):

- **Total Annual Loss:** Expected yearly loss in dollars and percentage
- **30-Year Present Value:** Discounted cumulative loss over 30 years
- **Hazard Breakdown:** Loss by hazard type (drought, flood, heat, precipitation, hurricane)

**Available for:**
- **Direct Risk:** Target country-sector location
- **Indirect Risk:** Aggregated supplier exposure (weighted by I-O coefficients)

---

## Endpoints

### 1. Health Check

**GET** `/api/health`

Check API status and model availability.

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "authentication": "enabled",
  "models": {
    "oecd": {
      "status": "available",
      "countries": 85,
      "sectors": 56
    },
    "exiobase": {
      "status": "partially_available",
      "note": "Coefficient matrix pending"
    }
  }
}
```

---

### 2. List Models

**GET** `/api/models`

Get available I-O models and their characteristics.

**Response:**
```json
{
  "oecd": {
    "name": "OECD ICIO Extended",
    "version": "2020",
    "countries": 85,
    "sectors": 56,
    "status": "available"
  },
  "exiobase": {
    "name": "EXIOBASE 3",
    "version": "2022",
    "regions": 49,
    "industries": 163,
    "status": "partially_available"
  }
}
```

---

### 3. List Countries

**GET** `/api/countries?model=oecd`

Get list of countries for a specific model.

**Parameters:**
- `model` (optional): `oecd` (default) or `exiobase`

**Response:**
```json
[
  {"code": "USA", "name": "United States"},
  {"code": "CHN", "name": "China"},
  {"code": "DEU", "name": "Germany"},
  ...
]
```

---

### 4. List Sectors

**GET** `/api/sectors?model=oecd`

Get list of sectors for a specific model.

**Parameters:**
- `model` (optional): `oecd` (default) or `exiobase`

**Response:**
```json
[
  {"code": "C10T12", "name": "Food products, beverages and tobacco"},
  {"code": "D26T27", "name": "Computer, electronic and optical products"},
  ...
]
```

---

### 5. Assess Risk

**GET** `/api/assess`

Comprehensive risk assessment for a country-sector combination.

**Parameters:**
- `country` (required): ISO country code (e.g., `USA`, `CHN`, `DEU`)
- `sector` (required): Sector code (e.g., `C10T12`, `D26T27`)
- `model` (optional): `oecd` (default) or `exiobase`
- `skip_climate` (optional): `true` or `false` (default: `false`)
  - `true`: Fast mode (~15s) - Core risk scores only
  - `false`: Comprehensive mode (~18s) - Includes expected loss data

**Example Request:**
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=USA&sector=C10T12&model=oecd&skip_climate=false"
```

**Response Structure:**
```json
{
  "country": {
    "code": "USA",
    "name": "United States"
  },
  "sector": {
    "code": "C10T12",
    "name": "Food products, beverages and tobacco"
  },
  "model": {
    "name": "OECD ICIO Extended",
    "version": "2020"
  },
  "direct_risk": {
    "climate": 3.10,
    "modern_slavery": 2.55,
    "nature_loss": 3.00,
    "political": 2.48,
    "water_stress": 3.20,
    "expected_loss": {
      "total_annual_loss": 8004.0,
      "total_annual_loss_pct": 0.8004,
      "present_value_30yr": 91457.44,
      "present_value_30yr_pct": 9.15,
      "breakdown": {
        "drought": {
          "annual_loss": 2760.0,
          "annual_loss_pct": 0.276,
          "confidence": "Regional Baseline",
          "details": "Average consecutive dry days: 110"
        },
        "flood": {
          "annual_loss": 1824.0,
          "annual_loss_pct": 0.1824,
          "confidence": "High",
          "details": "100-year flood depth: 1.14m, damage ratio: 22.8%"
        },
        ...
      }
    }
  },
  "indirect_risk": {
    "climate": 1.50,
    "modern_slavery": 1.28,
    "nature_loss": 1.47,
    "political": 1.24,
    "water_stress": 1.54,
    "expected_loss": {
      "total_annual_loss": 1727.0,
      "total_annual_loss_pct": 0.17,
      "present_value_30yr": 19745.0,
      "present_value_30yr_pct": 1.97,
      "breakdown": {
        "drought": {"annual_loss": 600.0, "annual_loss_pct": 0.06},
        "flood": {"annual_loss": 450.0, "annual_loss_pct": 0.045},
        ...
      },
      "note": "Supplier expected loss weighted by I-O coefficients from cached Climate API data"
    }
  },
  "total_risk": {
    "climate": 2.46,
    "modern_slavery": 2.04,
    "nature_loss": 2.39,
    "political": 1.98,
    "water_stress": 2.54
  },
  "top_suppliers": [
    {
      "country": "USA",
      "sector": "Wholesale and retail trade",
      "coefficient": 0.0895,
      "share": "8.95%"
    },
    ...
  ],
  "methodology": {
    "direct_risk_formula": "70% country risk + 30% sector risk",
    "indirect_risk_formula": "Weighted average of supplier total risks using I-O coefficients",
    "total_risk_formula": "60% direct risk + 40% indirect risk",
    "tier_weights": {
      "tier_1": "100%",
      "tier_2": "40%",
      "tier_3": "16%"
    },
    "max_tiers": 3
  }
}
```

**Response Fields:**

| Field | Description |
|-------|-------------|
| `direct_risk` | Inherent risk of target country-sector |
| `indirect_risk` | Weighted supplier risk across 3 tiers |
| `total_risk` | Combined exposure (60% direct + 40% indirect) |
| `expected_loss` | Financial impact estimates (only when `skip_climate=false`) |
| `top_suppliers` | Key supply chain dependencies with I-O coefficients |
| `methodology` | Calculation formulas and parameters |

**Using Expected Loss Data:**

For applications that need **supplier-specific financial impacts**, use the `indirect_risk.expected_loss` field:

```javascript
const response = await fetch(
  `${API_BASE_URL}/api/assess?country=USA&sector=C10T12&skip_climate=false`,
  { headers: { "X-API-Key": API_KEY } }
);

const data = await response.json();

// Direct exposure (target location)
const directLoss = data.direct_risk.expected_loss.total_annual_loss;

// Supplier exposure (supply chain)
const supplierLoss = data.indirect_risk.expected_loss.total_annual_loss;

// Total exposure
const totalLoss = directLoss + supplierLoss;
```

---

### 6. Batch Assessment

**POST** `/api/batch`

Assess multiple country-sector combinations in a single request.

**Request Body:**
```json
{
  "assessments": [
    {"country": "USA", "sector": "C10T12"},
    {"country": "CHN", "sector": "D26T27"},
    {"country": "DEU", "sector": "G45T47"}
  ],
  "model": "oecd",
  "skip_climate": false
}
```

**Response:**
```json
{
  "model": "oecd",
  "results": [
    {
      "country": "USA",
      "sector": "C10T12",
      "assessment": { ... }
    },
    ...
  ]
}
```

---

### 7. Cache Statistics

**GET** `/api/cache/stats`

Get expected loss cache statistics.

**Response:**
```json
{
  "cached_countries": 85,
  "countries": ["United States", "China", "Germany", ...]
}
```

---

### 8. Refresh Cache

**POST** `/api/cache/refresh?force=false`

Refresh pre-computed expected loss data for all countries.

**Parameters:**
- `force` (optional): `true` or `false` (default: `false`)
  - `false`: Only fetch missing countries
  - `true`: Re-fetch all countries (takes 15-20 minutes)

**Response:**
```json
{
  "status": "success",
  "message": "Cache refresh completed",
  "results": {
    "total": 85,
    "success": 85,
    "skipped": 0,
    "failed": []
  },
  "cache_stats": {
    "cached_countries": 85,
    "countries": [...]
  }
}
```

**Note:** This endpoint takes 15-20 minutes to complete when refreshing all countries.

---

## Integration Examples

### Python

```python
import requests

API_KEY = "zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM"
BASE_URL = "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com"

headers = {"X-API-Key": API_KEY}

# Assess risk
response = requests.get(
    f"{BASE_URL}/api/assess",
    params={
        "country": "USA",
        "sector": "C10T12",
        "model": "oecd",
        "skip_climate": "false"
    },
    headers=headers
)

data = response.json()

# Extract supplier expected loss
supplier_loss = data["indirect_risk"]["expected_loss"]["total_annual_loss"]
print(f"Supplier expected loss: ${supplier_loss:,.0f}")
```

### JavaScript

```javascript
const API_KEY = "zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM";
const BASE_URL = "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com";

async function assessRisk(country, sector) {
  const response = await fetch(
    `${BASE_URL}/api/assess?country=${country}&sector=${sector}&skip_climate=false`,
    { headers: { "X-API-Key": API_KEY } }
  );
  
  const data = await response.json();
  
  return {
    directLoss: data.direct_risk.expected_loss.total_annual_loss,
    supplierLoss: data.indirect_risk.expected_loss.total_annual_loss,
    totalRisk: data.total_risk.climate
  };
}

// Usage
const result = await assessRisk("USA", "C10T12");
console.log(`Supplier loss: $${result.supplierLoss.toLocaleString()}`);
```

### cURL

```bash
# Fast mode (15s) - Core risk scores only
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=USA&sector=C10T12&skip_climate=true"

# Comprehensive mode (18s) - Includes expected loss
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=USA&sector=C10T12&skip_climate=false"
```

---

## Data Sources

All risk assessments are based on real data from 12+ authoritative sources:

**Climate Risk:**
- NOAA Climate Data Online
- Copernicus Climate Data Store
- World Bank Climate Change Knowledge Portal

**Modern Slavery:**
- Walk Free Global Slavery Index 2023
- US Department of Labor TVPRA List
- IUCN Red List

**Political Risk:**
- World Bank Worldwide Governance Indicators
- FAO AQUASTAT Database

**Water Stress:**
- WRI Aqueduct Water Risk Atlas
- ILO ILOSTAT Database

**Nature Loss:**
- UNEP-WCMC Biodiversity Data
- Global Forest Watch

---

## Rate Limits

- **No hard rate limits** currently enforced
- Recommended: Max 10 requests/second
- Cache refresh endpoint: 1 request per 15 minutes

---

## Error Handling

**Error Response Format:**
```json
{
  "error": "Error description",
  "message": "Detailed error message",
  "country": "USA",
  "sector": "C10T12"
}
```

**Common Error Codes:**
- `400`: Missing or invalid parameters
- `401`: Missing or invalid API key
- `404`: Country-sector combination not found
- `500`: Internal server error

---

## Support

For questions, issues, or feature requests, contact the API maintainer or submit an issue to the project repository.

**Last Updated:** November 2025
