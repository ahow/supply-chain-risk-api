# Supply Chain Risk API - Integration Guide
## For External Applications and Developers

**Version**: 2.0.0  
**Last Updated**: November 17, 2025  
**Base URL**: `https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com`

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Request Examples](#request-examples)
5. [Response Format](#response-format)
6. [Code Examples](#code-examples)
7. [Error Handling](#error-handling)
8. [Rate Limits](#rate-limits)
9. [Best Practices](#best-practices)
10. [Support](#support)

---

## Quick Start

### Base URL
```
https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com
```

### API Key
```
zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM
```

### Simple Test Request
```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=USA&sector=D10T12"
```

---

## Authentication

All endpoints except `/` and `/api/health` require API key authentication.

### Method 1: HTTP Header (Recommended)

Include the API key in the request header:

```
X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM
```

**Example**:
```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/countries
```

### Method 2: Query Parameter

Include the API key as a query parameter:

```
?api_key=zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM
```

**Example**:
```bash
curl "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/countries?api_key=zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM"
```

**Note**: Method 1 (HTTP Header) is recommended for security reasons.

---

## API Endpoints

### 1. API Documentation

**Endpoint**: `GET /`  
**Authentication**: Not required  
**Description**: Returns API information and available endpoints

**Example**:
```bash
curl https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/
```

---

### 2. Health Check

**Endpoint**: `GET /api/health`  
**Authentication**: Not required  
**Description**: Check API status and data coverage

**Example**:
```bash
curl https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "Supply Chain Risk API",
  "version": "2.0.0",
  "authentication": "enabled",
  "data_coverage": {
    "countries": 67,
    "sectors": 34
  }
}
```

---

### 3. List Countries

**Endpoint**: `GET /api/countries`  
**Authentication**: Required  
**Description**: Get list of all 67 supported countries

**Example**:
```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/countries
```

**Response**:
```json
{
  "count": 67,
  "countries": [
    {
      "code": "USA",
      "name": "United States"
    },
    {
      "code": "CHN",
      "name": "China"
    },
    ...
  ]
}
```

---

### 4. List Sectors

**Endpoint**: `GET /api/sectors`  
**Authentication**: Required  
**Description**: Get list of all 34 OECD ICIO sectors

**Example**:
```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/sectors
```

**Response**:
```json
{
  "count": 34,
  "sectors": [
    {
      "code": "D01T03",
      "name": "Agriculture, forestry and fishing"
    },
    {
      "code": "D10T12",
      "name": "Food products, beverages and tobacco"
    },
    ...
  ]
}
```

---

### 5. Risk Assessment

**Endpoint**: `GET /api/assess`  
**Authentication**: Required  
**Description**: Comprehensive risk assessment for a country-sector combination

**Parameters**:
- `country` (required): ISO 3-letter country code (e.g., USA, CHN, DEU)
- `sector` (required): OECD ICIO sector code (e.g., D26T27, D10T12)

**Example**:
```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=CHN&sector=D26T27"
```

**Response**:
```json
{
  "country": "CHN",
  "country_name": "China",
  "sector": "D26T27",
  "sector_name": "Computer, electronic and optical products",
  "direct_risk": {
    "climate": 3.38,
    "modern_slavery": 3.77,
    "political": 3.93,
    "water_stress": 3.61,
    "nature_loss": 3.81
  },
  "indirect_risk": {
    "climate": 2.61,
    "modern_slavery": 2.64,
    "political": 2.75,
    "water_stress": 2.66,
    "nature_loss": 2.82
  },
  "total_risk": {
    "climate": 3.08,
    "modern_slavery": 3.31,
    "political": 3.45,
    "water_stress": 3.23,
    "nature_loss": 3.41
  },
  "climate_details": {
    "country": "China",
    "expected_annual_loss": 12500,
    "expected_annual_loss_pct": 1.25,
    "present_value_30y": 285000,
    "hazards": {
      "drought": 3200,
      "flood": 4100,
      "heat_stress": 2800,
      "hurricane": 0,
      "extreme_precipitation": 2400
    }
  },
  "top_suppliers": [
    {
      "country": "CHN",
      "sector": "D26T27",
      "coefficient": 0.2078,
      "country_name": "China",
      "sector_name": "Computer, electronic and optical products"
    },
    ...
  ],
  "methodology": {
    "direct_risk": "70% country risk + 30% sector risk",
    "indirect_risk": "Weighted average of supplier risks using I-O coefficients",
    "total_risk": "60% direct risk + 40% indirect risk",
    "tier_weights": "Tier-1: 100%, Tier-2: 40%, Tier-3: 16%"
  }
}
```

---

### 6. Batch Assessment

**Endpoint**: `POST /api/batch`  
**Authentication**: Required  
**Description**: Assess multiple country-sector combinations in a single request

**Request Body**:
```json
{
  "assessments": [
    {"country": "CHN", "sector": "D26T27"},
    {"country": "USA", "sector": "D10T12"},
    {"country": "DEU", "sector": "D29T30"}
  ]
}
```

**Example**:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  -d '{
    "assessments": [
      {"country": "CHN", "sector": "D26T27"},
      {"country": "USA", "sector": "D10T12"}
    ]
  }' \
  https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/batch
```

**Response**:
```json
{
  "count": 2,
  "results": [
    {
      "country": "CHN",
      "country_name": "China",
      "sector": "D26T27",
      "direct_risk": {...},
      "indirect_risk": {...},
      "total_risk": {...},
      ...
    },
    {
      "country": "USA",
      "country_name": "United States",
      "sector": "D10T12",
      "direct_risk": {...},
      "indirect_risk": {...},
      "total_risk": {...},
      ...
    }
  ]
}
```

---

## Request Examples

### Example 1: Get All Countries

```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/countries
```

### Example 2: Assess USA Food Manufacturing

```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=USA&sector=D10T12"
```

### Example 3: Assess China Electronics

```bash
curl -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/assess?country=CHN&sector=D26T27"
```

### Example 4: Batch Assessment

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-API-Key: zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM" \
  -d '{
    "assessments": [
      {"country": "CHN", "sector": "D26T27"},
      {"country": "USA", "sector": "D10T12"},
      {"country": "DEU", "sector": "D29T30"},
      {"country": "IND", "sector": "D13T15"}
    ]
  }' \
  https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/batch
```

---

## Response Format

### Risk Scores

All risk scores are on a **0-5 scale**:
- **0-1**: Very Low Risk
- **1-2**: Low Risk
- **2-3**: Medium Risk
- **3-4**: High Risk
- **4-5**: Very High Risk

### Risk Types

1. **Climate Risk**: Physical climate hazards (drought, flood, heat, hurricanes, precipitation)
2. **Modern Slavery Risk**: Forced labor, human trafficking, child labor
3. **Political Risk**: Governance quality, political stability, regulatory environment
4. **Water Stress Risk**: Water scarcity, quality, access
5. **Nature Loss Risk**: Biodiversity loss, ecosystem degradation, deforestation

### Risk Components

- **Direct Risk**: Inherent risk of the country-sector combination (70% country + 30% sector)
- **Indirect Risk**: Risk from suppliers weighted by I-O coefficients (multi-tier analysis)
- **Total Risk**: Combined exposure (60% direct + 40% indirect)

### Climate Details

For climate risk, additional quantitative metrics are provided:
- **Expected Annual Loss**: Dollar amount of expected annual loss
- **Expected Annual Loss %**: Percentage of GDP
- **Present Value (30y)**: 30-year present value of climate losses
- **Hazard Breakdown**: Loss breakdown by hazard type (drought, flood, heat stress, hurricane, extreme precipitation)

---

## Code Examples

### Python

```python
import requests

# API Configuration
BASE_URL = "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com"
API_KEY = "zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM"

# Set up headers
headers = {
    "X-API-Key": API_KEY
}

# Example 1: Get all countries
response = requests.get(f"{BASE_URL}/api/countries", headers=headers)
countries = response.json()
print(f"Total countries: {countries['count']}")

# Example 2: Single risk assessment
params = {
    "country": "CHN",
    "sector": "D26T27"
}
response = requests.get(f"{BASE_URL}/api/assess", headers=headers, params=params)
assessment = response.json()
print(f"Total Climate Risk: {assessment['total_risk']['climate']}")

# Example 3: Batch assessment
batch_data = {
    "assessments": [
        {"country": "CHN", "sector": "D26T27"},
        {"country": "USA", "sector": "D10T12"},
        {"country": "DEU", "sector": "D29T30"}
    ]
}
response = requests.post(
    f"{BASE_URL}/api/batch",
    headers=headers,
    json=batch_data
)
results = response.json()
print(f"Assessed {results['count']} country-sector combinations")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

// API Configuration
const BASE_URL = 'https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com';
const API_KEY = 'zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM';

// Set up headers
const headers = {
  'X-API-Key': API_KEY
};

// Example 1: Get all countries
async function getCountries() {
  const response = await axios.get(`${BASE_URL}/api/countries`, { headers });
  console.log(`Total countries: ${response.data.count}`);
  return response.data;
}

// Example 2: Single risk assessment
async function assessRisk(country, sector) {
  const response = await axios.get(`${BASE_URL}/api/assess`, {
    headers,
    params: { country, sector }
  });
  console.log(`Total Climate Risk: ${response.data.total_risk.climate}`);
  return response.data;
}

// Example 3: Batch assessment
async function batchAssess(assessments) {
  const response = await axios.post(
    `${BASE_URL}/api/batch`,
    { assessments },
    { headers }
  );
  console.log(`Assessed ${response.data.count} combinations`);
  return response.data;
}

// Usage
getCountries();
assessRisk('CHN', 'D26T27');
batchAssess([
  { country: 'CHN', sector: 'D26T27' },
  { country: 'USA', sector: 'D10T12' }
]);
```

### R

```r
library(httr)
library(jsonlite)

# API Configuration
BASE_URL <- "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com"
API_KEY <- "zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM"

# Set up headers
headers <- add_headers(`X-API-Key` = API_KEY)

# Example 1: Get all countries
response <- GET(paste0(BASE_URL, "/api/countries"), headers)
countries <- content(response, "parsed")
print(paste("Total countries:", countries$count))

# Example 2: Single risk assessment
response <- GET(
  paste0(BASE_URL, "/api/assess"),
  headers,
  query = list(country = "CHN", sector = "D26T27")
)
assessment <- content(response, "parsed")
print(paste("Total Climate Risk:", assessment$total_risk$climate))

# Example 3: Batch assessment
batch_data <- list(
  assessments = list(
    list(country = "CHN", sector = "D26T27"),
    list(country = "USA", sector = "D10T12")
  )
)
response <- POST(
  paste0(BASE_URL, "/api/batch"),
  headers,
  body = toJSON(batch_data, auto_unbox = TRUE),
  content_type_json()
)
results <- content(response, "parsed")
print(paste("Assessed", results$count, "combinations"))
```

### Excel / Power Query

```
let
    BaseURL = "https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com",
    APIKey = "zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM",
    
    // Get countries
    CountriesURL = BaseURL & "/api/countries",
    CountriesResponse = Web.Contents(
        CountriesURL,
        [Headers=[#"X-API-Key"=APIKey]]
    ),
    CountriesData = Json.Document(CountriesResponse),
    CountriesList = CountriesData[countries],
    CountriesTable = Table.FromList(
        CountriesList,
        Splitter.SplitByNothing(),
        null,
        null,
        ExtraValues.Error
    ),
    ExpandedCountries = Table.ExpandRecordColumn(
        CountriesTable,
        "Column1",
        {"code", "name"},
        {"Country Code", "Country Name"}
    )
in
    ExpandedCountries
```

---

## Error Handling

### HTTP Status Codes

- **200**: Success
- **400**: Bad Request (missing parameters)
- **401**: Unauthorized (missing API key)
- **403**: Forbidden (invalid API key)
- **404**: Not Found (invalid country/sector code)
- **500**: Internal Server Error

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Errors

**1. Missing API Key**
```json
{
  "error": "Authentication required",
  "message": "API key is required. Provide it via X-API-Key header or api_key query parameter."
}
```

**2. Invalid API Key**
```json
{
  "error": "Invalid API key",
  "message": "The provided API key is not valid"
}
```

**3. Invalid Country Code**
```json
{
  "error": "Country code XYZ not found"
}
```

**4. Missing Parameters**
```json
{
  "error": "Missing required parameters",
  "message": "Both country and sector parameters are required"
}
```

---

## Rate Limits

**Current Limits**:
- No hard rate limits currently enforced
- Recommended: Maximum 100 requests per minute
- Batch endpoint: Maximum 100 assessments per request

**Best Practices**:
- Use batch endpoint for multiple assessments
- Implement exponential backoff for retries
- Cache responses when appropriate

---

## Best Practices

### 1. Use Batch Endpoint for Multiple Assessments

Instead of:
```python
# Bad: Multiple individual requests
for country, sector in combinations:
    response = requests.get(f"{BASE_URL}/api/assess", ...)
```

Do this:
```python
# Good: Single batch request
batch_data = {
    "assessments": [
        {"country": c, "sector": s} for c, s in combinations
    ]
}
response = requests.post(f"{BASE_URL}/api/batch", ...)
```

### 2. Implement Error Handling

```python
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception for 4xx/5xx
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### 3. Cache Country and Sector Lists

```python
# Cache these lists - they don't change frequently
countries = get_countries()  # Cache for 24 hours
sectors = get_sectors()      # Cache for 24 hours
```

### 4. Use HTTP Header Authentication

```python
# Recommended
headers = {"X-API-Key": API_KEY}
response = requests.get(url, headers=headers)

# Not recommended (API key visible in logs)
response = requests.get(f"{url}?api_key={API_KEY}")
```

### 5. Handle First Request Delay

The API runs on Heroku free tier and may sleep after 30 minutes of inactivity. First request after sleep takes 10-30 seconds.

```python
import time

def call_api_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=60)
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise
```

---

## Data Coverage

### Countries (67 Total)

**OECD Members**: USA, CAN, MEX, CHL, COL, CRI, GBR, FRA, DEU, ITA, ESP, NLD, BEL, AUT, CHE, NOR, SWE, DNK, FIN, ISL, IRL, POL, CZE, HUN, SVK, SVN, EST, LVA, LTU, GRC, PRT, TUR, JPN, KOR, AUS, NZL, ISR

**OECD Partners**: CHN, IND, IDN, MYS, PHL, SGP, THA, VNM, HKG, TWN, KHM, BRN, BRA, ARG, PER, RUS, ROU, BGR, HRV, SAU, ZAF

### Sectors (34 Total)

**Primary**: D01T03 (Agriculture), D05T06 (Energy mining), D07T08 (Non-energy mining), D19 (Petroleum)

**Manufacturing**: D10T12 (Food), D13T15 (Textiles), D16 (Wood), D17T18 (Paper), D20T21 (Chemicals), D22 (Rubber & plastics), D23 (Non-metallic minerals), D24T25 (Metals), D26T27 (Electronics), D28 (Machinery), D29T30 (Transport equipment), D31T33 (Other manufacturing)

**Services**: D35T39 (Utilities), D41T43 (Construction), D45T47 (Trade), D49T53 (Transport), D55T56 (Accommodation & food), D58T60 (Publishing & media), D61 (Telecommunications), D62T63 (IT services), D64T66 (Finance), D68 (Real estate), D69T82 (Professional services), D84 (Public administration), D85 (Education), D86T88 (Health), D90T96 (Other services), D97T98 (Households)

Full lists available via `/api/countries` and `/api/sectors` endpoints.

---

## Support

### Technical Issues
- Check API health: `https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com/api/health`
- Review error messages in response body
- Verify API key is correct

### Questions or Issues
- Contact: andy.howard@schroders.com
- Heroku Dashboard: https://dashboard.heroku.com/apps/supply-chain-risk-api

### Additional Resources
- Manus Platform (Web Dashboard): https://supplyrisk-bb4n56uc.manus.space
- Climate Risk API: https://climate-risk-country-v4-fdee3b254d49.herokuapp.com

---

## Changelog

### Version 2.0.0 (November 17, 2025)
- Expanded coverage to 67 countries and 34 sectors
- Added API key authentication
- Implemented multi-tier supply chain analysis
- Integrated Climate Risk API V4 with expected loss calculations
- Added batch assessment endpoint
- Deployed to Heroku

---

**API URL**: `https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com`  
**API Key**: `zhSJ0IiDc1lb2qyOHK1rOkN20c4cXGRlNGSB4vhrNYM`

**Ready to integrate!** Use the code examples above to get started.
