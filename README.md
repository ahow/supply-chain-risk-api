# Supply Chain Risk Exposure Assessment API
## Standalone Flask REST API for Heroku

Comprehensive supply chain risk assessment framework providing independent exposure scores for 5 risk types across 67 countries and 34 OECD ICIO sectors.

---

## 🎯 Overview

This standalone Flask REST API provides:

- **5 Independent Risk Types**: Climate, Modern Slavery, Political Instability, Water Stress, Nature Loss
- **Dual Metrics**: Index-based scores (0-5 scale) + Expected losses (dollar amounts for climate)
- **Multi-Tier Analysis**: Tier-1 (100%), Tier-2 (40%), Tier-3 (16%) supplier weights
- **OECD ICIO Integration**: Comprehensive input-output coefficient matrix
- **Real Data Sources**: 12+ authoritative sources including NOAA, Walk Free GSI, ILO, World Bank
- **API Authentication**: Secure access with API key validation

---

## 📊 Coverage

- **67 Countries**: All OECD members + key partners (China, India, Brazil, Russia, etc.)
- **34 Sectors**: Full OECD ICIO classification (agriculture, manufacturing, services)
- **5 Risk Types**: Each independently assessed with separate scores

---

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py
```

The API will start on `http://localhost:5000`

### Deploy to Heroku

See [HEROKU_DEPLOYMENT_GUIDE.md](HEROKU_DEPLOYMENT_GUIDE.md) for complete instructions.

Quick deploy:

```bash
heroku create your-app-name
heroku config:set API_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
git push heroku main
```

---

## 🔑 Authentication

All endpoints except `/` and `/api/health` require API key authentication.

**Header Method (Recommended):**
```bash
curl -H "X-API-Key: your-api-key" \
  https://your-app.herokuapp.com/api/assess?country=CHN&sector=D26T27
```

**Query Parameter Method:**
```bash
curl "https://your-app.herokuapp.com/api/assess?country=CHN&sector=D26T27&api_key=your-api-key"
```

---

## 📡 API Endpoints

### GET /
API documentation and endpoint list

### GET /api/health
Health check (no auth required)

### GET /api/countries
List all 67 supported countries (auth required)

### GET /api/sectors
List all 34 OECD ICIO sectors (auth required)

### GET /api/assess
Risk assessment for country-sector combination (auth required)

**Parameters:**
- `country`: ISO 3-letter code (CHN, USA, DEU, etc.)
- `sector`: OECD ICIO code (D26T27, D10T12, etc.)

**Example:**
```bash
curl -H "X-API-Key: your-key" \
  "https://your-app.herokuapp.com/api/assess?country=CHN&sector=D26T27"
```

### POST /api/batch
Batch assessment for multiple combinations (auth required)

**Request Body:**
```json
{
  "assessments": [
    {"country": "CHN", "sector": "D26T27"},
    {"country": "USA", "sector": "D10T12"}
  ]
}
```

---

## 📁 Project Structure

```
heroku-risk-api/
├── app.py                          # Flask API server with authentication
├── risk_calculator.py              # Multi-tier risk calculation engine
├── io_coefficients.py              # I-O coefficient matrix (67×34)
├── oecd_data_full.py               # Full OECD countries and sectors data
├── climate_api_client.py           # Climate Risk API V4 integration
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment config
├── runtime.txt                     # Python version specification
├── README.md                       # This file
├── HEROKU_DEPLOYMENT_GUIDE.md      # Deployment instructions
└── API_DOCUMENTATION.md            # API reference
```

---

## 🧮 Methodology

### Direct Risk
Inherent risk of the country-sector combination:
- 70% country risk + 30% sector risk

### Indirect Risk
Weighted average of supplier risks using I-O coefficients:
- Tier-1 suppliers: 100% weight
- Tier-2 suppliers: 40% weight (suppliers' suppliers)
- Tier-3 suppliers: 16% weight (third-tier suppliers)

### Total Risk
Combined exposure:
- 60% direct risk + 40% indirect risk

---

## 📚 Data Sources

1. **Climate Risk**: NOAA, WRI Aqueduct, Climate Risk API V4
2. **Modern Slavery**: Walk Free Global Slavery Index 2023
3. **Political Risk**: World Bank Governance Indicators, Fragile States Index
4. **Water Stress**: WRI Aqueduct, FAO AQUASTAT
5. **Nature Loss**: IUCN Red List, WWF Living Planet Index

---

## 🔒 Security

- **API Key Authentication**: Required for all data endpoints
- **HTTPS Only**: Enforced by Heroku
- **Rate Limiting**: Recommended for production (add Flask-Limiter)
- **Environment Variables**: Never commit secrets to Git

---

## 🛠️ Development

### Testing

```bash
# Test risk calculator
python -c "from risk_calculator import MultiTierRiskCalculator; calc = MultiTierRiskCalculator(); print(calc.calculate_risk('USA', 'D26T27'))"

# Test Flask API
python app.py
# In another terminal:
curl http://localhost:5000/api/health
```

### Adding New Countries/Sectors

1. Update `oecd_data_full.py` with new entries
2. Update I-O coefficients in `io_coefficients.py` if needed
3. Test with `risk_calculator.py`
4. Redeploy to Heroku

---

## 📈 Performance

- **Response Time**: <2 seconds for single assessment
- **Batch Processing**: Up to 100 assessments per request
- **Concurrent Requests**: Scales with Heroku dyno type

---

## 🆘 Support

- **Deployment Issues**: See [HEROKU_DEPLOYMENT_GUIDE.md](HEROKU_DEPLOYMENT_GUIDE.md)
- **API Questions**: Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Data Accuracy**: Refer to data source documentation

---

## 📝 Version History

- **v2.0.0** (Current): Full OECD coverage (67 countries, 34 sectors), API authentication
- **v1.0.0**: Initial release with 5 sample countries

---

## 🔗 Related Projects

- **Manus Platform**: https://supplyrisk-bb4n56uc.manus.space (Full web dashboard)
- **Climate Risk API**: https://climate-risk-country-v4-fdee3b254d49.herokuapp.com

---

## 📄 License

Proprietary - Schroders Investment Management

---

## ✅ Status

- ✅ Full OECD coverage (67 countries, 34 sectors)
- ✅ Multi-tier supply chain analysis
- ✅ Climate API integration with expected losses
- ✅ API key authentication
- ✅ Ready for Heroku deployment
- ⏳ Awaiting user's Heroku credentials for deployment

---

**Ready to deploy!** Follow [HEROKU_DEPLOYMENT_GUIDE.md](HEROKU_DEPLOYMENT_GUIDE.md) for instructions.
