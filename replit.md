# Supply Chain Risk Assessment API

## Overview
A production-grade fullstack application that quantifies multi-dimensional supply chain risk exposure for any country-sector combination. Integrates 5 risk types (climate, modern slavery, political instability, water stress, nature loss) with input-output economic modeling.

## Architecture
- **Frontend**: React + Vite + Tailwind CSS + shadcn/ui + Recharts
- **Backend**: Express.js REST API
- **Data**: JSON-based risk datasets and I-O coefficient tables
- **Deployment**: Heroku (via GitHub)

## Key Files
- `shared/schema.ts` - All TypeScript types and Zod schemas
- `server/risk-calculator.ts` - Core risk assessment engine
- `server/routes.ts` - API endpoints
- `server/data/` - Risk scores, expected loss, I-O coefficients, countries, sectors
- `client/src/pages/dashboard.tsx` - Main dashboard page
- `client/src/components/` - Assessment form, radar chart, bar chart, risk badges, supplier table

## API Endpoints
- `GET /api/health` - Health check
- `GET /api/countries` - List all countries
- `GET /api/sectors` - List all sectors
- `GET /api/assess?country=USA&sector=B06` - Full risk assessment

## Deployment
- **GitHub**: https://github.com/ahow/supply-chain-risk-api
- **Heroku**: https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com
- Push to GitHub triggers deployment via Heroku builds API
- Buildpack: heroku/nodejs
- Procfile: `web: npm run start`

## Recent Changes
- 2026-02-15: Full rebuild in Node.js/Express/React stack
- Risk calculator with OECD I-O coefficient modeling
- 85 countries, 52 sectors, 5 risk dimensions
- Dashboard with radar charts, hazard breakdown, supplier table
