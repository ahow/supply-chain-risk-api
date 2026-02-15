# Supply Chain Risk Assessment API

## Overview
A production-grade fullstack application that quantifies multi-dimensional supply chain risk exposure for any country-sector combination. Integrates 5 risk types (climate, modern slavery, political instability, water stress, nature loss) with input-output economic modeling.

## Architecture
- **Frontend**: React + Vite + Tailwind CSS + shadcn/ui + Recharts
- **Backend**: Express.js REST API
- **Data**: JSON-based risk datasets and I-O coefficient tables
- **Deployment**: Heroku (via GitHub)

## Key Files
- `shared/schema.ts` - All TypeScript types and Zod schemas (including LLM provider types)
- `server/risk-calculator.ts` - Core risk assessment engine
- `server/llm-service.ts` - Multi-LLM analysis service (Gemini, Claude, DeepSeek, MiniMax)
- `server/routes.ts` - API endpoints
- `server/data/` - Risk scores, expected loss, I-O coefficients, countries, sectors
- `client/src/pages/dashboard.tsx` - Main dashboard page
- `client/src/components/` - Assessment form, radar chart, bar chart, risk badges, supplier table, AI analysis panel

## API Endpoints
- `GET /api/health` - Health check
- `GET /api/countries` - List all countries
- `GET /api/sectors` - List all sectors
- `GET /api/assess?country=USA&sector=B06` - Full risk assessment
- `GET /api/llm-providers` - List available LLM providers
- `POST /api/analyze` - Run LLM analysis on assessment data (body: {provider, assessmentData})

## LLM Integration
- 4 providers: Gemini (gemini-2.5-flash), Claude (claude-sonnet-4), DeepSeek (deepseek-chat), MiniMax (MiniMax-M2.5)
- Secrets required: GEMINI_API_KEY, CLAUDE_API_KEY, DEEPSEEK_API_KEY, MINIMAX_API_KEY
- Tracks response time, token usage, and estimated cost per request
- Comparison metrics panel when multiple models have been queried

## Deployment
- **GitHub**: https://github.com/ahow/supply-chain-risk-api
- **Heroku**: https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com
- Push to GitHub triggers deployment via Heroku builds API
- Buildpack: heroku/nodejs
- Procfile: `web: npm run start`

## Recent Changes
- 2026-02-15: Added multi-LLM AI analysis integration (Gemini, Claude, DeepSeek, MiniMax) with cost/speed comparison
- 2026-02-15: Full rebuild in Node.js/Express/React stack
- Risk calculator with OECD I-O coefficient modeling
- 85 countries, 52 sectors, 5 risk dimensions
- Dashboard with radar charts, hazard breakdown, supplier table
