# Heroku Deployment Guide
## Supply Chain Risk Exposure Assessment API

Complete guide for deploying the standalone Flask REST API to Heroku with full OECD coverage (67 countries, 34 sectors) and API authentication.

---

## 📋 Prerequisites

1. **Heroku Account**: Sign up at https://heroku.com
2. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-cli
3. **Git**: Ensure Git is installed on your system

---

## 🚀 Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

This will open your browser for authentication.

### 2. Create Heroku App

```bash
cd /path/to/heroku-risk-api
heroku create your-app-name
```

Replace `your-app-name` with your desired app name (e.g., `supply-chain-risk-api`). If you omit the name, Heroku will generate a random one.

### 3. Generate and Set API Key

Generate a secure API key:

```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

This will output a secure random key like: `Xk7mP2nQ9vR4sT6wY8zA1bC3dE5fG7hJ9kL0mN2oP4qR6sT8u`

Set it as an environment variable in Heroku:

```bash
heroku config:set API_KEY=your-generated-api-key-here
```

**Important**: Save this API key securely - you'll need it to access the API.

### 4. Deploy to Heroku

Initialize Git repository (if not already done):

```bash
git init
git add .
git commit -m "Initial deployment: Supply Chain Risk API with full OECD coverage"
```

Push to Heroku:

```bash
git push heroku main
```

If your default branch is `master`:

```bash
git push heroku master
```

### 5. Verify Deployment

Check if the app is running:

```bash
heroku ps
heroku logs --tail
```

Open the app in your browser:

```bash
heroku open
```

---

## 🔑 API Authentication

The API uses API key authentication for all endpoints except `/` and `/api/health`.

### Authentication Methods

**Option 1: HTTP Header (Recommended)**

```bash
curl -H "X-API-Key: your-api-key-here" \
  https://your-app-name.herokuapp.com/api/assess?country=CHN&sector=D26T27
```

**Option 2: Query Parameter**

```bash
curl "https://your-app-name.herokuapp.com/api/assess?country=CHN&sector=D26T27&api_key=your-api-key-here"
```

### Disabling Authentication (Not Recommended for Production)

To disable authentication (for testing only):

```bash
heroku config:unset API_KEY
```

---

## 📡 API Endpoints

### 1. Home / Documentation
```
GET /
```
Returns API documentation and available endpoints. **No authentication required.**

### 2. Health Check
```
GET /api/health
```
Returns API health status. **No authentication required.**

### 3. List Countries
```
GET /api/countries
```
Returns all 67 supported countries. **Requires authentication.**

**Example:**
```bash
curl -H "X-API-Key: your-api-key" \
  https://your-app-name.herokuapp.com/api/countries
```

### 4. List Sectors
```
GET /api/sectors
```
Returns all 34 OECD ICIO sectors. **Requires authentication.**

**Example:**
```bash
curl -H "X-API-Key: your-api-key" \
  https://your-app-name.herokuapp.com/api/sectors
```

### 5. Risk Assessment
```
GET /api/assess?country={ISO3}&sector={CODE}
```
Comprehensive risk assessment for a country-sector combination. **Requires authentication.**

**Parameters:**
- `country`: ISO 3-letter country code (e.g., CHN, USA, DEU)
- `sector`: OECD ICIO sector code (e.g., D26T27, D10T12, D01T03)

**Example:**
```bash
curl -H "X-API-Key: your-api-key" \
  "https://your-app-name.herokuapp.com/api/assess?country=CHN&sector=D26T27"
```

**Response Structure:**
```json
{
  "country": "CHN",
  "country_name": "China",
  "sector": "D26T27",
  "sector_name": "Computer, electronic and optical products",
  "direct_risk": {
    "climate": 3.2,
    "modern_slavery": 3.8,
    "political": 3.5,
    "water_stress": 3.6,
    "nature_loss": 3.4
  },
  "indirect_risk": {
    "climate": 2.9,
    "modern_slavery": 3.2,
    "political": 3.1,
    "water_stress": 3.0,
    "nature_loss": 2.8
  },
  "total_risk": {
    "climate": 3.08,
    "modern_slavery": 3.56,
    "political": 3.34,
    "water_stress": 3.36,
    "nature_loss": 3.16
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
      "coefficient": 0.2000,
      "country_name": "China",
      "sector_name": "Computer, electronic and optical products"
    }
  ],
  "methodology": {
    "direct_risk": "70% country risk + 30% sector risk",
    "indirect_risk": "Weighted average of supplier risks using I-O coefficients",
    "total_risk": "60% direct risk + 40% indirect risk",
    "tier_weights": "Tier-1: 100%, Tier-2: 40%, Tier-3: 16%"
  }
}
```

### 6. Batch Assessment
```
POST /api/batch
```
Assess multiple country-sector combinations in a single request. **Requires authentication.**

**Request Body:**
```json
{
  "assessments": [
    {"country": "CHN", "sector": "D26T27"},
    {"country": "USA", "sector": "D10T12"},
    {"country": "DEU", "sector": "D29T30"}
  ]
}
```

**Example:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"assessments":[{"country":"CHN","sector":"D26T27"},{"country":"USA","sector":"D10T12"}]}' \
  https://your-app-name.herokuapp.com/api/batch
```

---

## 🔧 Configuration

### Environment Variables

View all config vars:
```bash
heroku config
```

Set a new config var:
```bash
heroku config:set VARIABLE_NAME=value
```

### Required Environment Variables

- `API_KEY`: API authentication key (required for production)
- `PORT`: Port number (automatically set by Heroku)

### Optional Environment Variables

- `HEROKU_RELEASE_CREATED_AT`: Deployment timestamp (automatically set by Heroku)

---

## 📊 Data Coverage

### Countries (67 Total)

**OECD Members:**
- Americas: USA, CAN, MEX, CHL, COL, CRI
- Europe: AUT, BEL, CZE, DNK, EST, FIN, FRA, DEU, GRC, HUN, ISL, IRL, ITA, LVA, LTU, LUX, NLD, NOR, POL, PRT, SVK, SVN, ESP, SWE, CHE, TUR, GBR
- Asia-Pacific: AUS, JPN, KOR, NZL, ISR

**OECD Partners:**
- Asia: CHN, IND, IDN, MYS, PHL, SGP, THA, VNM, HKG, TWN, KHM, BRN
- Americas: BRA, ARG, PER
- Europe: RUS, ROU, BGR, HRV
- Middle East: SAU
- Africa: ZAF

### Sectors (34 Total)

Based on OECD ICIO classification:
- Primary: Agriculture (D01T03), Mining (D05T06, D07T08), Energy (D19)
- Manufacturing: Food (D10T12), Textiles (D13T15), Chemicals (D20T21), Metals (D24T25), Electronics (D26T27), Transport Equipment (D29T30), etc.
- Services: Construction (D41T43), Trade (D45T47), Transport (D49T53), Finance (D64T66), Professional Services (D69T82), Public Services (D84T88)

Full sector list available at: `/api/sectors`

---

## 🔍 Monitoring & Debugging

### View Logs

Real-time logs:
```bash
heroku logs --tail
```

Last 100 lines:
```bash
heroku logs -n 100
```

### Check App Status

```bash
heroku ps
```

### Restart App

```bash
heroku restart
```

### Scale Dynos

```bash
heroku ps:scale web=1
```

---

## 🚨 Troubleshooting

### Issue: "Application Error" on Heroku

**Solution:**
1. Check logs: `heroku logs --tail`
2. Verify all files are committed: `git status`
3. Ensure `requirements.txt` is up to date
4. Verify `Procfile` exists and is correct

### Issue: "Authentication Required" Error

**Solution:**
1. Verify API key is set: `heroku config:get API_KEY`
2. Check API key in request header or query parameter
3. Ensure key matches exactly (no extra spaces)

### Issue: Module Import Errors

**Solution:**
1. Verify all Python files are in the repository
2. Check `requirements.txt` includes all dependencies
3. Redeploy: `git push heroku main --force`

### Issue: Slow Response Times

**Solution:**
1. Upgrade to Hobby dyno: `heroku ps:type hobby`
2. Enable caching for frequently accessed data
3. Consider using Redis for caching (add-on)

---

## 💰 Cost Considerations

### Free Tier
- 550-1000 free dyno hours per month
- App sleeps after 30 minutes of inactivity
- Wakes up on first request (may take 10-30 seconds)

### Hobby Tier ($7/month)
- Never sleeps
- Better performance
- SSL certificates included

### Upgrade Command
```bash
heroku ps:type hobby
```

---

## 🔒 Security Best Practices

1. **Always use API key authentication in production**
   ```bash
   heroku config:set API_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
   ```

2. **Use HTTPS only** (Heroku provides this automatically)

3. **Rotate API keys regularly**
   ```bash
   heroku config:set API_KEY=new-key-here
   ```

4. **Monitor access logs**
   ```bash
   heroku logs --tail | grep "api_key"
   ```

5. **Rate limiting** (consider adding Flask-Limiter for production)

---

## 📚 Additional Resources

- **Heroku Documentation**: https://devcenter.heroku.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Manus Platform**: https://supplyrisk-bb4n56uc.manus.space
- **API Reference**: See `API_REFERENCE.md` in project root

---

## 🆘 Support

For issues with:
- **Heroku deployment**: Check Heroku documentation or contact Heroku support
- **API functionality**: Review API_REFERENCE.md or check application logs
- **Data accuracy**: Refer to data source documentation in the main platform

---

## 📝 Version History

- **v2.0.0** (Current): Full OECD coverage (67 countries, 34 sectors), API authentication, Climate API integration
- **v1.0.0**: Initial release with 5 sample countries

---

## ✅ Deployment Checklist

Before going live:

- [ ] Heroku app created
- [ ] API key generated and set in Heroku config
- [ ] Code deployed successfully (`git push heroku main`)
- [ ] Health check endpoint responding (`/api/health`)
- [ ] Authentication working (test with valid/invalid keys)
- [ ] Sample risk assessment successful
- [ ] Logs showing no errors (`heroku logs --tail`)
- [ ] API key saved securely for distribution to users
- [ ] Documentation updated with actual Heroku URL
- [ ] Consider upgrading to Hobby dyno for production use

---

## 🎯 Next Steps After Deployment

1. **Test the API**
   ```bash
   curl -H "X-API-Key: your-key" https://your-app.herokuapp.com/api/health
   ```

2. **Update API_REFERENCE.md** with your Heroku URL

3. **Share API key** with authorized users securely

4. **Monitor usage** via Heroku dashboard

5. **Set up custom domain** (optional)
   ```bash
   heroku domains:add api.yourdomain.com
   ```

---

## Integration with Manus Platform

Both deployments can coexist:

- **Manus URL**: https://supplyrisk-bb4n56uc.manus.space/api/trpc (tRPC protocol, web dashboard)
- **Heroku URL**: https://your-app.herokuapp.com/api (REST protocol, standalone API)

Use Manus for the full web dashboard, Heroku for standalone API access and infrastructure independence.

---

**Deployment Complete!** 🎉

Your Supply Chain Risk API is now live at: `https://your-app-name.herokuapp.com`
