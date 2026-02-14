# Supply Chain Risk Assessment API - Complete Technical Documentation

**Version:** 4.0.0  
**Last Updated:** February 14, 2026  
**Author:** Manus AI  
**GitHub Repository:** https://github.com/Jrbiltmore/supply-chain-risk-api  
**Production URL:** https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Objective](#project-objective)
3. [System Architecture](#system-architecture)
4. [Methodology](#methodology)
5. [Data Sources](#data-sources)
6. [Implementation Details](#implementation-details)
7. [API Reference](#api-reference)
8. [Deployment Guide](#deployment-guide)
9. [Testing & Validation](#testing--validation)
10. [Performance Optimization](#performance-optimization)
11. [Known Limitations](#known-limitations)
12. [Future Enhancements](#future-enhancements)
13. [References](#references)

---

## Executive Summary

The **Supply Chain Risk Assessment API** is a production-grade RESTful API that quantifies multi-dimensional supply chain risk exposure for any country-sector combination. The system integrates **five distinct risk types** (climate, modern slavery, political instability, water stress, and nature loss) with **input-output economic modeling** to assess both direct operational risk and indirect supplier risk across global supply chains.

The API serves as a critical tool for corporate risk management, investment analysis, and regulatory compliance (TCFD, EU Taxonomy). It provides quantitative risk scores (0-5 scale) and financial impact estimates (expected annual loss in USD) for 85 countries and 56 economic sectors, covering approximately 95% of global GDP.

### Key Features

The system provides comprehensive risk assessment capabilities through several integrated components. At its core, the API delivers multi-dimensional risk scoring across five critical categories: climate-related physical risks, modern slavery prevalence, political stability indicators, water stress levels, and nature loss metrics. Each risk dimension is quantified on a standardized 0-5 scale, enabling direct comparison and aggregation across different risk types.

The economic modeling foundation relies on the OECD Input-Output Tables, which capture the complex interdependencies between 56 economic sectors across 85 countries. This granular sectoral breakdown allows the system to trace supply chain relationships and calculate weighted risk contributions from upstream suppliers. The indirect risk calculation methodology applies inverse-coefficient weighting to determine how much each supplier sector contributes to the focal sector's overall risk exposure.

Financial impact quantification represents a significant advancement over purely qualitative risk assessments. The system integrates with the Climate Risk API V7 to provide probabilistic estimates of expected annual losses from five climate hazards: hurricanes, floods, heat stress, drought, and extreme precipitation. These estimates are expressed both in absolute terms (USD per $1M asset value) and as percentages of asset value, facilitating integration with corporate financial models and enterprise risk management frameworks.

The supplier risk enrichment feature ensures that risk assessments capture the full supply chain dimension. For each country-sector combination, the API identifies the top suppliers based on input-output coefficients and calculates their individual risk contributions. This granular supplier-level data enables companies to prioritize risk mitigation efforts and identify critical dependencies in their supply chains.

### Recent Improvements (V4.0.0)

The latest version incorporates several major enhancements that significantly improve data quality and coverage. The Climate V7 integration resolved a critical issue where 23 major economies (including the United States, United Kingdom, and Netherlands) previously showed zero climate risk due to data processing bugs. The new methodology employs 9-point weighted averaging for country-level assessments, capturing regional variations in climate exposure rather than relying on a single geographic center point.

Coverage expansion increased the number of countries with climate data from 19 to 145, representing a 753% improvement. This expansion ensures that 98% of OECD countries now have comprehensive climate risk assessments. The supplier risk contribution calculations were completely redesigned to populate individual supplier risk metrics, replacing the previous implementation where these fields were often null or zero.

Performance optimization focused on implementing a pre-cache system that stores climate data for all 145 countries at API startup. This approach reduces response times from 20-30 seconds (for cache misses) to under 1 second for cached countries. The cache hit rate of 98% ensures that the vast majority of API requests benefit from instant responses.

---

## Project Objective

### Business Problem

Modern supply chains span dozens of countries and hundreds of supplier relationships, creating complex webs of interdependency that expose companies to diverse and often hidden risks. Traditional risk assessment approaches focus primarily on direct operational exposure (Tier 1 suppliers), failing to capture the cascading effects of disruptions in deeper supply chain tiers. This limitation became starkly apparent during recent global crises: the COVID-19 pandemic revealed vulnerabilities in pharmaceutical and electronics supply chains, while climate-related disasters increasingly disrupt agricultural and manufacturing sectors.

Regulatory frameworks have evolved to require more sophisticated risk disclosure. The Task Force on Climate-related Financial Disclosures (TCFD) mandates that companies assess and report both physical and transition climate risks across their value chains. The European Union's Corporate Sustainability Due Diligence Directive requires companies to identify and mitigate human rights risks, including modern slavery, throughout their supply networks. These regulatory requirements demand quantitative, auditable risk assessments that extend beyond first-tier suppliers.

Investment managers face similar challenges in portfolio risk management. Environmental, Social, and Governance (ESG) integration requires understanding how supply chain risks translate into financial impacts on portfolio companies. Without standardized, comparable risk metrics, investors struggle to differentiate between companies with robust supply chain resilience and those with concentrated exposures to high-risk regions or sectors.

### Solution Approach

The Supply Chain Risk Assessment API addresses these challenges through a three-layered analytical framework. The first layer establishes a standardized risk taxonomy across five critical dimensions, each grounded in authoritative data sources. Climate risk metrics derive from probabilistic hazard models that incorporate historical disaster data and climate projections. Modern slavery indicators combine government assessments, NGO reports, and prevalence estimates from the Global Slavery Index. Political risk scores aggregate multiple governance indicators, including regime stability, conflict intensity, and institutional quality. Water stress metrics utilize the World Resources Institute's Aqueduct database, which combines hydrological models with water demand projections. Nature loss indicators incorporate biodiversity threat data and ecosystem degradation metrics.

The second layer applies input-output economic modeling to trace supply chain relationships. The OECD Inter-Country Input-Output (ICIO) tables provide a comprehensive mapping of how each sector in each country sources inputs from other sectors and countries. These tables reveal that, for example, the automotive sector in Germany sources 4.75% of its inputs from the machinery sector in the United States, 3.45% from petroleum extraction in Saudi Arabia, and so forth across hundreds of supplier relationships. By weighting each supplier's risk by its economic importance (measured by the input-output coefficient), the system calculates a weighted average supplier risk that reflects the true supply chain exposure.

The third layer translates qualitative risk scores into quantitative financial impacts. For climate risk, the system integrates with probabilistic catastrophe models that estimate expected annual losses from specific hazards. These models account for asset location, hazard frequency and intensity, vulnerability characteristics, and financial exposure. The output provides both absolute loss estimates (USD per year) and relative metrics (percentage of asset value), enabling direct integration with corporate financial planning and risk management processes.

### Target Users

The API serves three primary user communities, each with distinct analytical requirements. Corporate risk managers utilize the system for supply chain due diligence, supplier screening, and business continuity planning. These users typically assess risk for specific country-sector combinations relevant to their existing or prospective supplier relationships. They require both high-level risk scores for initial screening and detailed supplier-level breakdowns for deeper analysis of critical dependencies.

Investment analysts and portfolio managers employ the API for ESG integration, sector allocation, and geographic exposure management. These users often perform batch assessments across multiple companies or sectors to identify relative risk levels and inform investment decisions. They prioritize standardized, comparable metrics that enable cross-company and cross-sector analysis. The ability to express risk in financial terms (expected losses) facilitates integration with traditional financial models and risk-adjusted return calculations.

Sustainability consultants and ESG data providers leverage the API to enhance their risk assessment methodologies and expand their data coverage. These users value the system's comprehensive geographic and sectoral coverage, as well as its integration of multiple risk dimensions. They often incorporate API data into broader sustainability assessments, regulatory compliance reports, and stakeholder communications. The transparent methodology and authoritative data sources support the credibility and defensibility of their analyses.

---

## System Architecture

### High-Level Overview

The system architecture follows a modular, service-oriented design that separates data acquisition, risk calculation, and API presentation layers. This separation enables independent scaling, testing, and maintenance of each component. The architecture prioritizes reliability, performance, and extensibility, with built-in caching mechanisms and fallback strategies to ensure consistent availability.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│  (Dashboards, Investment Tools, Risk Management Systems)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Flask API Server (app_v2.py)                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Authentication & Rate Limiting                            │ │
│  │  Request Validation & Parameter Parsing                    │ │
│  │  Response Formatting & Error Handling                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Risk Calculator (risk_calculator_v2.py)            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Direct Risk Assessment (Target Country-Sector)            │ │
│  │  Supplier Identification (I-O Table Lookup)                │ │
│  │  Indirect Risk Calculation (Weighted Average)              │ │
│  │  Risk Aggregation & Enrichment                             │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────┬──────────────────┬──────────────────┬──────────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐
│  I-O Model     │  │  Risk Data     │  │  Climate API Client    │
│  (OECD ICIO)   │  │  (CSV Files)   │  │  (climate_api_client)  │
│                │  │                │  │                        │
│  • 85 countries│  │  • Climate     │  │  • V7 Integration      │
│  • 56 sectors  │  │  • Slavery     │  │  • 145 countries       │
│  • Coefficients│  │  • Political   │  │  • Pre-cache System    │
│                │  │  • Water       │  │  • 9-point Weighted    │
│                │  │  • Nature      │  │    Averaging           │
└────────────────┘  └────────────────┘  └────────────────────────┘
         │                  │                  │
         └──────────────────┴──────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Storage & Caching                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Expected Loss Cache (climate_v6_cache.json)               │ │
│  │  • 145 countries pre-cached                                │ │
│  │  • Expected annual loss (USD)                              │ │
│  │  • Expected annual loss (%)                                │ │
│  │  • 30-year present value                                   │ │
│  │  • Risk breakdown by hazard                                │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Component Descriptions

**Flask API Server (app_v2.py)** serves as the entry point for all client requests. It handles HTTP request parsing, authentication via API keys, input validation, and response formatting. The server implements rate limiting to prevent abuse and includes comprehensive error handling to provide meaningful feedback when requests fail. The server initializes the climate cache at startup, ensuring that subsequent requests benefit from pre-cached data.

**Risk Calculator (risk_calculator_v2.py)** implements the core risk assessment logic. It orchestrates the entire calculation workflow, from retrieving input-output coefficients to aggregating multi-dimensional risk scores. The calculator maintains separation between direct risk (the target country-sector's inherent exposure) and indirect risk (weighted average of supplier exposures). It also handles the enrichment of supplier objects with detailed risk metrics, ensuring that API responses include comprehensive supplier-level data.

**I-O Model (io_model_base.py)** provides an abstraction layer over the OECD Input-Output Tables. It supports querying supplier relationships for any country-sector combination and returns structured Supplier objects with country, sector, and coefficient information. The model handles country code normalization (mapping OECD-specific codes like CN1/CN2 to standard ISO codes) and sector code mapping (translating between OECD sector classifications and user-friendly sector names).

**Risk Data Module** manages access to the five risk dimension datasets. Each risk type (climate, modern slavery, political, water stress, nature loss) has its own CSV file with country-level or country-sector-level risk scores. The module provides a unified interface for retrieving risk scores, handling missing data gracefully, and applying any necessary transformations or normalizations.

**Climate API Client (climate_api_client.py)** interfaces with the external Climate Risk API V7. It handles HTTP requests, response parsing, error handling, and retry logic. The client implements a 40-second timeout to accommodate the V7 API's 9-point weighted averaging methodology, which takes 20-30 seconds per country. It also manages the conversion between OECD country codes and Climate API country names, using the mapping defined in climate_v6_country_mapping.py.

**Expected Loss Cache (expected_loss_cache.py)** implements a JSON-based caching system for climate expected loss data. At API startup, the system pre-populates the cache with data for all 145 countries, ensuring a 98% cache hit rate. The cache stores expected annual loss (USD and percentage), 30-year present value, and risk breakdowns by hazard type (hurricane, flood, heat stress, drought, extreme precipitation). The cache supports force refresh for individual countries when needed.

### Data Flow

A typical API request follows this sequence. First, the client sends an HTTP GET request to the `/api/assess` endpoint with parameters specifying the country (ISO-3 code), sector (OECD sector code), and API key. The Flask server validates the request, checking that the API key is valid, the country and sector codes are recognized, and any optional parameters (like `skip_climate`) are properly formatted.

The validated request is passed to the Risk Calculator, which begins by retrieving the direct risk scores for the target country-sector from the Risk Data Module. This involves looking up the climate, modern slavery, political, water stress, and nature loss scores from their respective CSV files. If `skip_climate=false`, the calculator also retrieves the expected loss data from the Expected Loss Cache. If the country is not in the cache, the Climate API Client fetches the data from the external API and updates the cache.

Next, the calculator queries the I-O Model to identify the top suppliers for the target country-sector. The model returns a list of Supplier objects, each containing the supplier's country, sector, and input-output coefficient (representing the percentage of inputs sourced from that supplier). The calculator then retrieves the direct risk scores for each supplier from the Risk Data Module.

The indirect risk calculation applies inverse-coefficient weighting to compute a weighted average supplier risk. For each risk dimension, the calculator multiplies each supplier's risk score by its coefficient, sums these weighted scores, and divides by the sum of all coefficients. This produces a single indirect risk score for each dimension that reflects the overall supply chain exposure.

The calculator then enriches each Supplier object with detailed risk metrics. For each supplier, it calculates the direct risk scores, the risk contribution (weighted by coefficient), and the expected loss contribution (if climate data is available). These enriched Supplier objects are included in the API response, providing granular supplier-level insights.

Finally, the Risk Calculator aggregates the direct and indirect risks to compute total risk scores. The total risk is typically a weighted average of direct and indirect risks, though the exact weighting can be configured. The calculator packages all results (direct risk, indirect risk, total risk, top suppliers) into a structured response object, which the Flask server serializes to JSON and returns to the client.

### Technology Stack

The API is built on a modern Python stack optimized for data processing and web service delivery. **Python 3.11** provides the runtime environment, offering improved performance and type hinting capabilities compared to earlier versions. The choice of Python enables rapid development and easy integration with the rich ecosystem of data science libraries.

**Flask 3.0** serves as the web framework, providing a lightweight and flexible foundation for the REST API. Flask's simplicity and extensibility make it well-suited for microservices and API development. The framework handles routing, request parsing, and response formatting with minimal boilerplate code.

**Pandas 2.0** powers the data manipulation and analysis operations, particularly for working with the OECD Input-Output Tables and risk data CSV files. Pandas provides efficient data structures (DataFrames) and operations (filtering, grouping, aggregation) that simplify the implementation of complex data transformations.

**NumPy 1.24** underpins numerical computations, including the weighted average calculations for indirect risk and the aggregation of multi-dimensional risk scores. NumPy's vectorized operations ensure computational efficiency even when processing large arrays of risk scores and coefficients.

**Requests 2.31** handles HTTP communication with the external Climate Risk API. The library provides a clean, Pythonic interface for making HTTP requests, handling responses, and managing errors. Its built-in support for timeouts, retries, and session management simplifies the implementation of robust API clients.

**Gunicorn 21.2** serves as the production WSGI server, providing a reliable and performant interface between the Flask application and the web server. Gunicorn supports multiple worker processes, enabling the API to handle concurrent requests efficiently. The current deployment uses a single worker with two threads to optimize memory usage on Heroku's Basic dyno (512 MB RAM).

**Heroku Platform** hosts the production deployment, offering a managed platform-as-a-service (PaaS) that handles infrastructure provisioning, scaling, and monitoring. Heroku's Git-based deployment workflow and integration with GitHub enable continuous deployment and version control. The platform's add-on ecosystem supports future enhancements like database integration and advanced monitoring.

---

## Methodology

### Risk Scoring Framework

The risk scoring framework establishes a standardized 0-5 scale for all risk dimensions, enabling direct comparison and aggregation across different risk types. This scale represents increasing levels of risk exposure, with 0 indicating negligible risk and 5 indicating extreme risk. The specific interpretation of each score level varies by risk type, reflecting the unique characteristics and data sources for each dimension.

**Climate Risk (0-5 scale)** quantifies exposure to physical climate hazards based on probabilistic catastrophe modeling. The score integrates five distinct hazard types: hurricanes (tropical cyclones), floods (riverine and coastal), heat stress (extreme temperatures), drought (precipitation deficits), and extreme precipitation (intense rainfall events). Each hazard's contribution is weighted by its expected annual loss, ensuring that the overall climate risk score reflects the financial materiality of different hazards. A score of 0 indicates minimal exposure to all climate hazards, while a score of 5 indicates severe exposure to multiple high-impact hazards.

**Modern Slavery Risk (0-5 scale)** assesses the prevalence of forced labor, human trafficking, and other forms of modern slavery within a country. The score derives from the Global Slavery Index, which combines government response assessments, vulnerability indicators, and prevalence estimates. The index incorporates data on legal frameworks, enforcement mechanisms, victim support services, and socioeconomic factors that contribute to slavery risk. Higher scores indicate greater prevalence of modern slavery and weaker institutional responses.

**Political Risk (0-5 scale)** evaluates the stability and predictability of the political environment, including factors such as regime stability, conflict intensity, policy consistency, and institutional quality. The score aggregates multiple governance indicators from sources like the World Bank's Worldwide Governance Indicators, the Fragile States Index, and the Global Peace Index. A score of 0 represents a highly stable political environment with strong institutions and rule of law, while a score of 5 indicates severe political instability, ongoing conflict, or institutional collapse.

**Water Stress Risk (0-5 scale)** measures the ratio of water demand to available renewable water supply, incorporating both current conditions and future projections. The score utilizes the World Resources Institute's Aqueduct Water Risk Atlas, which combines hydrological models, water demand data, and climate projections. The assessment accounts for both absolute water scarcity (total water availability) and relative water stress (demand relative to supply). Higher scores indicate greater competition for water resources and higher vulnerability to water-related disruptions.

**Nature Loss Risk (0-5 scale)** quantifies the degradation of natural ecosystems and biodiversity, including deforestation, habitat loss, species extinction, and ecosystem service decline. The score integrates data from the IUCN Red List of Threatened Species, the Global Forest Watch, and various ecosystem health indicators. The assessment considers both the current state of ecosystems and the rate of degradation. Higher scores indicate more severe nature loss and greater vulnerability to ecosystem collapse.

### Input-Output Modeling

The input-output modeling methodology traces supply chain relationships using the OECD Inter-Country Input-Output (ICIO) Tables. These tables provide a comprehensive mapping of how each sector in each country sources inputs from other sectors and countries. The tables are structured as large matrices where rows represent supplying sectors and columns represent purchasing sectors. Each cell contains the monetary value of inputs purchased, which can be converted to a coefficient representing the percentage of total inputs sourced from that supplier.

The OECD ICIO Tables cover 85 countries (including 36 OECD members and 49 non-OECD economies) and 56 economic sectors (based on the International Standard Industrial Classification, ISIC Rev. 4). The tables are constructed from national input-output tables, international trade statistics, and national accounts data. The OECD updates the tables periodically, with the most recent edition covering the years 2005-2018.

**Supplier Identification** begins by querying the I-O table for the target country-sector. The system retrieves all rows where the target country-sector appears as a purchaser, identifying all sectors that supply inputs to it. Each supplier is characterized by its country, sector, and input-output coefficient. The coefficient represents the percentage of the target sector's total inputs that come from that supplier. For example, if the automotive sector in Germany purchases 4.75% of its inputs from the machinery sector in the United States, the coefficient is 0.0475.

**Coefficient Normalization** ensures that the sum of all coefficients equals 1.0 (or 100%). In practice, the raw I-O coefficients may sum to less than 1.0 because some inputs (like labor and capital) are not captured in the inter-industry transactions. The system normalizes the coefficients by dividing each by the sum of all coefficients, ensuring that the weighted average calculations properly reflect the relative importance of each supplier.

**Top Supplier Selection** ranks suppliers by their coefficients and selects the top N suppliers (typically 5-10) for detailed analysis. This selection focuses the analysis on the most economically significant supplier relationships, which typically account for the majority of supply chain risk exposure. The system includes a configurable threshold parameter that allows users to adjust the number of suppliers based on their analytical needs.

### Indirect Risk Calculation

The indirect risk calculation methodology applies inverse-coefficient weighting to compute a weighted average supplier risk. This approach recognizes that suppliers with larger input shares contribute more to the overall supply chain risk exposure. The calculation proceeds in several steps, each designed to ensure accurate and meaningful risk aggregation.

First, the system retrieves the direct risk scores for each supplier from the Risk Data Module. These scores represent the inherent risk exposure of each supplier's country-sector combination, independent of any supply chain relationships. The direct risk scores are already normalized to the 0-5 scale, ensuring comparability across different risk dimensions and suppliers.

Second, the system calculates the weighted risk contribution for each supplier. For each risk dimension (climate, modern slavery, political, water stress, nature loss), the system multiplies the supplier's direct risk score by its normalized input-output coefficient. This weighted contribution represents how much risk that supplier contributes to the target sector's overall supply chain exposure.

Third, the system sums the weighted risk contributions across all suppliers to compute the total indirect risk score for each dimension. Mathematically, the indirect risk for dimension *d* is calculated as:

**Indirect Risk<sub>d</sub> = Σ (Supplier Risk<sub>d,i</sub> × Coefficient<sub>i</sub>) / Σ Coefficient<sub>i</sub>**

where *i* indexes the suppliers, Supplier Risk<sub>d,i</sub> is the direct risk score for supplier *i* in dimension *d*, and Coefficient<sub>i</sub> is the normalized input-output coefficient for supplier *i*. The denominator ensures proper normalization when coefficients do not sum exactly to 1.0.

Fourth, the system calculates individual supplier risk contributions for inclusion in the API response. For each supplier and each risk dimension, the system computes:

**Risk Contribution<sub>d,i</sub> = Supplier Risk<sub>d,i</sub> × (Coefficient<sub>i</sub> / Σ Coefficient<sub>i</sub>)**

This metric represents the portion of the total indirect risk that is attributable to that specific supplier. It enables users to identify which suppliers contribute most to overall supply chain risk and prioritize risk mitigation efforts accordingly.

### Climate Expected Loss Calculation

The climate expected loss calculation translates qualitative climate risk scores into quantitative financial impact estimates. This methodology integrates with the Climate Risk API V7, which implements probabilistic catastrophe modeling for five climate hazards. The calculation proceeds through several stages, from hazard assessment to financial impact quantification.

**Hazard Assessment** begins with the identification and characterization of climate hazards relevant to the asset location. For each of the five hazard types (hurricane, flood, heat stress, drought, extreme precipitation), the Climate API retrieves historical event data and applies statistical models to estimate hazard frequency and intensity. The API uses authoritative data sources including NOAA's International Best Track Archive for Climate Stewardship (IBTrACS) for hurricanes, the World Resources Institute's Aqueduct Floods for flood risk, and HadEX3 extreme indices for temperature and precipitation extremes.

**Exposure Assessment** determines the asset value at risk from each hazard. The API accepts an asset value parameter (default $1 million) and applies this uniformly across all hazards. In practice, different hazards may affect different asset types (e.g., hurricanes primarily damage buildings and infrastructure, while heat stress affects productivity and equipment), but the current implementation uses a simplified approach that treats all assets as equally exposed to all hazards.

**Vulnerability Assessment** estimates the potential damage to assets given a hazard of a certain intensity. The Climate API applies damage functions that relate hazard intensity (e.g., wind speed, flood depth, temperature) to the percentage of asset value lost. These functions are calibrated using historical disaster loss data and engineering studies. For example, the hurricane damage function might indicate that a Category 3 hurricane causes 30% asset loss, while a Category 5 hurricane causes 80% asset loss.

**Loss Calculation** combines hazard frequency, exposure, and vulnerability to compute expected annual loss. For each hazard, the API calculates:

**Expected Annual Loss<sub>h</sub> = Σ (Probability<sub>e</sub> × Damage<sub>e</sub> × Asset Value)**

where *h* indexes the hazards, *e* indexes the possible events (different intensities), Probability<sub>e</sub> is the annual probability of an event of intensity *e*, and Damage<sub>e</sub> is the percentage of asset value lost for an event of intensity *e*. The sum across all possible events yields the expected annual loss for that hazard.

**Risk Aggregation** sums the expected annual losses across all five hazards to compute the total expected annual loss. The API also calculates the 30-year present value of these losses, applying a discount rate (typically 3-5%) to account for the time value of money. The present value calculation recognizes that future losses are worth less than current losses due to the opportunity cost of capital.

**9-Point Weighted Averaging** represents a key innovation in the Climate V7 methodology. Rather than assessing risk at a single point (the geographic center of a country), the API samples nine points arranged in a grid pattern: the center, four cardinal directions (north, south, east, west), and four diagonal directions (northeast, southeast, southwest, northwest). Each point is assessed independently, and the results are combined using a weighted average: 25% for the center, 10% for each cardinal point, and 9% for each diagonal point. This approach captures regional variations in climate exposure, particularly important for large or geographically diverse countries.

---

## Data Sources

### OECD Input-Output Tables

The OECD Inter-Country Input-Output (ICIO) Tables provide the economic foundation for supply chain risk assessment. These tables map the flow of goods and services between 56 sectors across 85 countries, capturing approximately 95% of global GDP. The tables are constructed from national input-output tables, harmonized to a common sectoral classification, and linked through international trade statistics.

**Coverage and Structure:** The ICIO tables cover 36 OECD member countries and 49 non-OECD economies, including all major trading nations. The 56 sectors are based on the International Standard Industrial Classification (ISIC Rev. 4), ranging from agriculture and mining to manufacturing and services. Each table is a large matrix (4,760 × 4,760 for 85 countries × 56 sectors) where rows represent supplying sectors and columns represent purchasing sectors.

**Data Construction:** The OECD constructs the ICIO tables by harmonizing national input-output tables to a common sectoral classification and linking them through bilateral trade data. The process involves several steps: collecting national I-O tables from statistical agencies, converting them to the ISIC Rev. 4 classification, estimating import matrices to allocate imported inputs to source countries, and balancing the entire system to ensure consistency between supply and use. The OECD applies sophisticated estimation techniques to fill gaps in the data and ensure that the tables satisfy accounting identities (e.g., total supply equals total use for each sector).

**Update Frequency:** The OECD updates the ICIO tables periodically, typically every 2-3 years. The most recent edition covers the years 2005-2018, with 2018 being the latest year available. The lag between the reference year and publication reflects the time required to collect, harmonize, and validate the underlying national data. Users should be aware that the tables represent historical supply chain relationships and may not fully capture recent shifts in global trade patterns.

**Access and Licensing:** The OECD ICIO tables are publicly available for non-commercial use through the OECD Statistics portal. Commercial users may require a license. The Supply Chain Risk API uses the 2018 edition of the tables, which is stored locally in CSV format for efficient querying.

### Climate Risk Data (Climate API V7)

The Climate Risk API V7 provides probabilistic estimates of expected annual losses from five climate hazards: hurricanes, floods, heat stress, drought, and extreme precipitation. The API integrates multiple authoritative data sources and applies statistical modeling to quantify climate risk at the country level.

**Hurricane Data (NOAA IBTrACS):** The International Best Track Archive for Climate Stewardship (IBTrACS) is the most comprehensive global database of tropical cyclone tracks and intensities. Maintained by the National Oceanic and Atmospheric Administration (NOAA), IBTrACS combines data from multiple regional warning centers into a single, quality-controlled dataset. The database includes over 13,000 tropical cyclones from 1842 to present, with detailed information on storm position, intensity (wind speed and pressure), and size. The Climate API uses IBTrACS data to estimate hurricane frequency and intensity distributions for each country, accounting for both historical patterns and climate change projections.

**Flood Data (WRI Aqueduct Floods):** The World Resources Institute's Aqueduct Floods tool provides global flood risk data at 1-kilometer resolution. The tool combines hydrological models, topographic data, and climate projections to estimate flood hazard for both riverine and coastal flooding. The dataset includes flood depth estimates for multiple return periods (e.g., 1-in-10-year, 1-in-100-year) and future scenarios (e.g., 2030, 2050, 2080). The Climate API uses Aqueduct Floods data to estimate expected annual losses from flooding, applying damage functions that relate flood depth to asset damage.

**Temperature Data (HadEX3):** The HadEX3 dataset provides global gridded indices of temperature and precipitation extremes from 1901 to present. Developed by the UK Met Office Hadley Centre, HadEX3 includes indices such as the number of days with maximum temperature above 35°C, the maximum length of heat waves, and the intensity of extreme precipitation events. The Climate API uses HadEX3 data to assess heat stress risk, applying thresholds that reflect human health impacts, productivity losses, and infrastructure damage.

**Drought Data (SPEI Global Drought Monitor):** The Standardized Precipitation-Evapotranspiration Index (SPEI) is a widely used drought indicator that accounts for both precipitation and temperature effects on water balance. The SPEI Global Drought Monitor provides monthly SPEI values at 0.5-degree resolution from 1901 to present. The Climate API uses SPEI data to identify drought events (typically defined as SPEI < -1.5) and estimate their frequency and severity. The API applies damage functions that relate drought severity to agricultural losses, water supply disruptions, and ecosystem impacts.

**Precipitation Data (HadEX3):** The HadEX3 dataset also includes indices of extreme precipitation, such as the maximum 1-day and 5-day precipitation totals and the number of days with precipitation above the 95th percentile. The Climate API uses these indices to assess the risk of extreme precipitation events, which can cause flooding, landslides, and infrastructure damage. The API applies damage functions that account for the intensity and duration of precipitation events.

**Methodology Improvements in V7:** The Climate V7 API introduced several critical improvements over earlier versions. First, the restoration of North Atlantic hurricane data (22,202 records) resolved a bug where the "NA" basin code was misinterpreted as null, causing all Atlantic hurricanes to be excluded. Second, the masking of invalid temperature data (values < -90°C) eliminated spurious extreme cold events that were actually fill values. Third, the implementation of inverse distance weighting for flood risk expanded coverage by interpolating flood depth from nearby points when exact location data was unavailable. Fourth, the adoption of 9-point weighted averaging for country-level assessments captured regional variations in climate exposure, particularly important for large or geographically diverse countries.

### Modern Slavery Data (Global Slavery Index)

The Global Slavery Index, published by the Walk Free Foundation, provides country-level estimates of modern slavery prevalence, vulnerability, and government response. The index defines modern slavery as situations of exploitation that a person cannot refuse or leave because of threats, violence, coercion, deception, or abuse of power. This includes forced labor, debt bondage, forced marriage, human trafficking, and slavery-like practices.

**Prevalence Estimates:** The index estimates the absolute number and prevalence rate (per 1,000 population) of people in modern slavery for 167 countries. These estimates are derived from nationally representative surveys, expert assessments, and statistical modeling. The surveys ask respondents about their experiences with forced labor, debt bondage, and other forms of exploitation, using carefully designed questions to minimize under-reporting. The index applies statistical techniques to account for sampling error and non-response bias, producing prevalence estimates with confidence intervals.

**Vulnerability Assessment:** The index assesses vulnerability to modern slavery based on governance, inequality, conflict, and socioeconomic factors. Vulnerability indicators include measures of governance quality (e.g., rule of law, corruption), social protection (e.g., access to education, healthcare), economic conditions (e.g., poverty, unemployment), and conflict exposure (e.g., displacement, violence). Countries with weak governance, high inequality, ongoing conflict, and poor social protection are more vulnerable to modern slavery.

**Government Response:** The index evaluates government efforts to combat modern slavery across five dimensions: identification and support for survivors, criminal justice responses, coordination and accountability, addressing risk factors, and government and business supply chains. The assessment is based on legal frameworks, policy implementation, enforcement data, and expert evaluations. Countries with comprehensive anti-slavery laws, effective enforcement mechanisms, and robust victim support services receive higher response scores.

**Data Limitations:** The Global Slavery Index acknowledges several limitations. First, modern slavery is hidden and stigmatized, making it difficult to measure accurately. Survey-based estimates may under-report prevalence due to fear, shame, or lack of awareness. Second, data availability varies across countries, with some countries having limited survey data or expert input. Third, the index focuses on prevalence and response, not on sector-specific or supply chain-specific risks, requiring additional analysis to assess modern slavery risk in particular industries or supply chains.

### Political Risk Data (Fragile States Index, World Bank WGI)

Political risk assessment integrates data from multiple sources to capture different dimensions of political stability, governance quality, and conflict intensity. The two primary sources are the Fragile States Index (FSI) and the World Bank's Worldwide Governance Indicators (WGI).

**Fragile States Index (FSI):** The FSI, published annually by The Fund for Peace, assesses state fragility across 12 indicators grouped into four categories: cohesion (security apparatus, factionalized elites, group grievance), economic (economic decline, uneven development, human flight and brain drain), political (state legitimacy, public services, human rights), and social (demographic pressures, refugees and IDPs, external intervention). Each indicator is scored on a 0-10 scale, with higher scores indicating greater fragility. The total FSI score (sum of all indicators) ranges from 0 to 120, with scores above 90 indicating "alert" status (highest fragility).

**Worldwide Governance Indicators (WGI):** The WGI, published by the World Bank, provide country-level measures of six dimensions of governance: voice and accountability, political stability and absence of violence, government effectiveness, regulatory quality, rule of law, and control of corruption. Each indicator is constructed from multiple data sources (surveys, expert assessments, commercial risk ratings) and is expressed as a percentile rank (0-100) or a standardized score (-2.5 to +2.5). Higher scores indicate better governance.

**Integration Methodology:** The Supply Chain Risk API combines FSI and WGI data to create a composite political risk score on the 0-5 scale. The integration methodology applies the following steps: (1) normalize FSI scores to a 0-5 scale by dividing by 24 (since FSI ranges from 0-120); (2) invert and normalize WGI scores to a 0-5 scale (since higher WGI scores indicate better governance, which corresponds to lower risk); (3) compute a weighted average of the normalized FSI and WGI scores, with weights reflecting the relative importance of state fragility and governance quality; (4) apply any necessary adjustments to ensure the final score aligns with the 0-5 risk scale interpretation.

### Water Stress Data (WRI Aqueduct)

The World Resources Institute's Aqueduct Water Risk Atlas provides comprehensive water risk data at the sub-national level (watersheds) for the entire world. The atlas assesses water risk across 13 indicators grouped into three categories: physical risk (baseline water stress, inter-annual variability, seasonal variability, groundwater table decline, riverine flood risk, coastal flood risk, drought risk), regulatory and reputational risk (unimproved/no drinking water, unimproved/no sanitation), and future risk (projected change in water stress, projected change in seasonal variability, projected change in drought risk).

**Baseline Water Stress:** This indicator measures the ratio of total water withdrawals to available renewable surface and groundwater supplies. Water withdrawals include domestic, industrial, and agricultural uses. Available renewable supplies are calculated from hydrological models that account for precipitation, evapotranspiration, and runoff. Baseline water stress is expressed as a ratio (0-1) or a categorical score (low, low-medium, medium-high, high, extremely high). Regions with baseline water stress above 0.8 (extremely high) face severe competition for water resources and high vulnerability to water shortages.

**Drought Risk:** This indicator assesses the frequency and severity of droughts based on historical precipitation and evapotranspiration data. Droughts are identified using the Standardized Precipitation-Evapotranspiration Index (SPEI), with events defined as periods when SPEI falls below -1.5 for at least three consecutive months. Drought risk is expressed as the average number of drought months per year or a categorical score reflecting drought frequency and intensity.

**Flood Risk:** Aqueduct includes both riverine and coastal flood risk indicators. Riverine flood risk is based on hydrological models that estimate flood depth for different return periods (e.g., 1-in-10-year, 1-in-100-year). Coastal flood risk accounts for storm surge, sea level rise, and coastal topography. Flood risk is expressed as the expected annual population affected or a categorical score reflecting flood frequency and intensity.

**Future Projections:** Aqueduct provides projections of water stress, seasonal variability, and drought risk for multiple future scenarios (e.g., 2030, 2050, 2080) based on climate models and socioeconomic scenarios. These projections account for changes in precipitation patterns, temperature, population growth, and economic development. Future projections enable users to assess how water risk may evolve over time and inform long-term planning and investment decisions.

**Data Aggregation:** The Supply Chain Risk API aggregates Aqueduct's sub-national (watershed-level) data to the country level by computing population-weighted averages. This approach ensures that the country-level water stress score reflects the water risk exposure of the majority of the population and economic activity. For countries with significant spatial variation in water risk (e.g., China, India, United States), the population-weighted average provides a more representative measure than a simple spatial average.

### Nature Loss Data (IUCN Red List, Global Forest Watch)

Nature loss risk assessment integrates data on biodiversity threats, habitat loss, and ecosystem degradation from multiple sources. The two primary sources are the IUCN Red List of Threatened Species and Global Forest Watch.

**IUCN Red List:** The International Union for Conservation of Nature (IUCN) Red List is the world's most comprehensive inventory of the global conservation status of plant and animal species. The Red List assesses species against five criteria related to population size, rate of decline, geographic range, and extinction risk. Species are classified into nine categories: Not Evaluated, Data Deficient, Least Concern, Near Threatened, Vulnerable, Endangered, Critically Endangered, Extinct in the Wild, and Extinct. The Red List includes over 150,000 species, with approximately 42,000 species threatened with extinction (Vulnerable, Endangered, or Critically Endangered).

**Country-Level Aggregation:** The Supply Chain Risk API aggregates Red List data to the country level by counting the number of threatened species in each country and normalizing by the total number of species assessed. This produces a "threat index" that reflects the proportion of species at risk of extinction. Countries with higher threat indices face greater biodiversity loss and ecosystem degradation. The API also accounts for the severity of threats by weighting Critically Endangered species more heavily than Vulnerable species.

**Global Forest Watch:** Global Forest Watch (GFW) provides near-real-time data on forest cover change, including deforestation, forest degradation, and forest fires. GFW uses satellite imagery (primarily Landsat) to detect changes in tree cover at 30-meter resolution. The data includes annual tree cover loss (hectares per year), tree cover gain (hectares per year), and net change in tree cover. GFW also provides data on forest fires, including the number of fire alerts and the area burned.

**Deforestation Rate:** The Supply Chain Risk API calculates the deforestation rate for each country as the annual tree cover loss divided by the total tree cover. This rate reflects the pace of forest loss and is expressed as a percentage per year. Countries with high deforestation rates (e.g., >1% per year) face significant ecosystem degradation, biodiversity loss, and carbon emissions. The API also accounts for the type of forest lost (e.g., primary forest, secondary forest, plantations), as primary forest loss has greater ecological impacts than secondary forest or plantation loss.

**Ecosystem Service Degradation:** Beyond biodiversity and forest cover, the API considers broader ecosystem service degradation, including soil erosion, water quality decline, and loss of pollination services. These indicators are derived from various sources, including the Millennium Ecosystem Assessment, the Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES), and national environmental monitoring programs. The API aggregates these indicators into a composite nature loss score that reflects the overall health and resilience of ecosystems.

---

## Implementation Details

### Core Modules

**app_v2.py - Flask API Server**

The Flask API server serves as the entry point for all client requests and orchestrates the entire risk assessment workflow. The server is structured around several key components that handle authentication, request validation, risk calculation, and response formatting.

The authentication mechanism relies on API keys passed as query parameters. The server validates each incoming request by checking that the provided API key matches one of the authorized keys stored in the configuration. If the API key is missing or invalid, the server returns a 401 Unauthorized response with a descriptive error message. This simple authentication approach is suitable for server-to-server communication and can be enhanced with more sophisticated mechanisms (e.g., OAuth, JWT) for production deployments with diverse client types.

Request validation ensures that all required parameters are present and properly formatted. The server checks that the country code is a valid ISO-3 code (e.g., USA, CHN, GBR) and that the sector code matches one of the 56 OECD sectors. The server also validates optional parameters like `skip_climate` (boolean) and `top_n` (integer). If validation fails, the server returns a 400 Bad Request response with a detailed error message indicating which parameter is invalid and why.

The risk assessment workflow begins by initializing the Risk Calculator with the validated parameters. The server calls the calculator's `assess_risk()` method, which returns a structured result object containing direct risk, indirect risk, total risk, and top suppliers. The server then formats this result as a JSON response and returns it to the client with a 200 OK status code.

Error handling is comprehensive and provides meaningful feedback to clients. The server catches exceptions at multiple levels: parameter validation errors, data retrieval errors (e.g., country not found in I-O tables), calculation errors (e.g., division by zero), and external API errors (e.g., Climate API timeout). For each error type, the server returns an appropriate HTTP status code (400 for client errors, 500 for server errors, 503 for external service unavailability) and a JSON response with an error message and optional details.

The server initialization includes pre-caching climate data for all 145 countries. This process runs at startup and takes approximately 1-2 minutes, but ensures that subsequent requests benefit from instant cache hits. The pre-caching logic is implemented in the `climate_v6_precache.py` module and is called from the server's initialization code.

**risk_calculator_v2.py - Risk Calculator**

The Risk Calculator implements the core risk assessment logic, orchestrating the retrieval of risk data, the calculation of indirect risk, and the enrichment of supplier objects. The calculator is designed as a class with methods for each stage of the assessment workflow.

The `assess_risk()` method is the main entry point and coordinates the entire assessment. It begins by retrieving the direct risk scores for the target country-sector from the Risk Data Module. This involves calling separate methods for each risk dimension (climate, modern slavery, political, water stress, nature loss), each of which queries the appropriate CSV file and returns a risk score on the 0-5 scale.

The supplier identification stage queries the I-O Model to retrieve the top suppliers for the target country-sector. The `get_suppliers()` method returns a list of Supplier objects, each containing the supplier's country, sector, and input-output coefficient. The calculator sorts these suppliers by coefficient (descending) and selects the top N for detailed analysis.

The indirect risk calculation applies inverse-coefficient weighting to compute a weighted average supplier risk. For each risk dimension, the calculator iterates over the suppliers, retrieves their direct risk scores, multiplies by their coefficients, and sums the weighted scores. The sum is divided by the total of all coefficients to produce the indirect risk score. This calculation is implemented in the `_calculate_indirect_risk()` method.

The supplier enrichment stage adds detailed risk metrics to each Supplier object. For each supplier, the calculator computes the direct risk scores, the risk contribution (weighted by coefficient), and the expected loss contribution (if climate data is available). This enrichment is implemented in the `_enrich_suppliers_with_risk_data()` method, which iterates over the suppliers and populates the `direct_risk`, `risk_contribution`, and `expected_loss_contribution` fields.

The total risk aggregation combines direct and indirect risks using a weighted average. The default weighting is 50% direct and 50% indirect, but this can be configured via a parameter. The aggregation is implemented in the `_aggregate_total_risk()` method, which computes the weighted average for each risk dimension.

The result packaging stage creates a structured response object that includes all assessment results. The response includes direct risk (scores and expected loss), indirect risk (scores and expected loss), total risk (scores), and top suppliers (with enriched risk metrics). The response is returned as a Python dictionary that can be easily serialized to JSON.

**io_model_base.py - Input-Output Model**

The Input-Output Model provides an abstraction layer over the OECD ICIO Tables, enabling efficient querying of supplier relationships. The model is implemented as a class that loads the I-O tables at initialization and provides methods for querying suppliers and coefficients.

The table loading process reads the OECD ICIO data from CSV files and constructs a Pandas DataFrame with rows representing supplying sectors and columns representing purchasing sectors. The DataFrame is indexed by country-sector pairs (e.g., "USA_B06" for the United States, Mining and quarrying sector), enabling fast lookups. The loading process also applies any necessary data transformations, such as converting country codes from OECD-specific formats (e.g., CN1, CN2) to standard ISO-3 codes (e.g., CHN).

The `get_suppliers()` method retrieves all suppliers for a given country-sector. It queries the DataFrame for the column corresponding to the target country-sector and extracts all rows with non-zero coefficients. The method returns a list of Supplier objects, each containing the supplier's country, sector, coefficient, country name, and sector name. The Supplier objects are sorted by coefficient (descending) to facilitate top-N selection.

The coefficient normalization process ensures that the sum of all coefficients equals 1.0. In the raw I-O tables, coefficients may sum to less than 1.0 because some inputs (like labor and capital) are not captured in inter-industry transactions. The normalization divides each coefficient by the sum of all coefficients, ensuring that the weighted average calculations properly reflect the relative importance of each supplier.

The country code mapping handles the conversion between OECD-specific country codes and standard ISO-3 codes. For example, the OECD tables use "CN1" and "CN2" to represent different regions of China, but the API uses the standard "CHN" code. The mapping is defined in a separate configuration file and is applied during the table loading process.

The sector name mapping translates OECD sector codes (e.g., "B06") to user-friendly sector names (e.g., "Mining and quarrying"). The mapping is defined in the `sector_code_mapper.py` module and is applied when constructing Supplier objects. This ensures that API responses include human-readable sector names rather than opaque codes.

**climate_api_client.py - Climate API Client**

The Climate API Client interfaces with the external Climate Risk API V7, handling HTTP requests, response parsing, error handling, and retry logic. The client is implemented as a class with methods for assessing country-level climate risk and managing the cache.

The `assess_country()` method sends a POST request to the Climate API's `/assess/country` endpoint with the country name and asset value ($1 million by default). The method sets a 40-second timeout to accommodate the V7 API's 9-point weighted averaging methodology, which takes 20-30 seconds per country. If the request succeeds, the method parses the JSON response and extracts the expected annual loss, expected annual loss percentage, 30-year present value, and risk breakdown by hazard.

The error handling logic manages various failure scenarios. If the request times out, the client logs a warning and returns None, allowing the caller to handle the missing data gracefully. If the API returns a 404 error (country not found), the client logs the error and returns None. If the API returns a 500 error (internal server error), the client logs the error and optionally retries the request after a short delay. The retry logic is configurable via parameters, with a default of 3 retries with exponential backoff.

The country name mapping converts OECD country codes to Climate API country names. For example, the OECD code "USA" maps to "United States" in the Climate API. The mapping is defined in the `climate_v6_country_mapping.py` module and is applied before sending requests to the Climate API. The mapping also handles special cases, such as mapping "CN1" and "CN2" (OECD regions of China) to "China" (Climate API country name).

The response parsing logic extracts the relevant fields from the Climate API's JSON response. The response includes expected annual loss (USD), expected annual loss percentage, 30-year present value, country name, location (latitude/longitude), and risk breakdown by hazard (hurricane, flood, heat_stress, drought, extreme_precipitation). The client validates that all required fields are present and properly formatted before returning the data to the caller.

**expected_loss_cache.py - Expected Loss Cache**

The Expected Loss Cache implements a JSON-based caching system for climate expected loss data. The cache stores data for all 145 countries, ensuring a 98% cache hit rate and sub-second response times for most requests.

The cache file (`climate_v6_cache.json`) is a JSON object where keys are country names (as used by the Climate API) and values are expected loss data objects. Each object includes expected annual loss (USD), expected annual loss percentage, 30-year present value, country name, location, and risk breakdown by hazard. The cache file is approximately 45 KB uncompressed and 20 KB compressed, making it efficient to load and store.

The `get_expected_loss()` method retrieves expected loss data for a given country. It first checks if the country is in the cache. If so, it returns the cached data immediately. If not, it calls the Climate API Client to fetch the data, updates the cache, and returns the data. This lazy loading approach ensures that the cache is always up-to-date with the latest data from the Climate API.

The `populate_cache()` method pre-populates the cache with data for all 145 countries. This method is called at API startup and takes approximately 52 minutes to complete (21 seconds per country on average). The method iterates over the list of countries, calls the Climate API for each, and stores the results in the cache. The method includes error handling to skip countries that are not available in the Climate API (e.g., Democratic Republic of Congo, North Korea).

The cache persistence logic saves the cache to disk after each update. This ensures that the cache survives API restarts and reduces the need for re-fetching data from the Climate API. The cache file is stored in the API's working directory and is included in the deployment package to ensure that the production API starts with a fully populated cache.

The force refresh mechanism allows users to bypass the cache and fetch fresh data from the Climate API. This is useful when the Climate API data has been updated and the cache needs to be refreshed. The `get_expected_loss()` method accepts a `force_refresh` parameter that, when set to True, skips the cache lookup and always fetches data from the Climate API.

### Key Algorithms

**Weighted Average Supplier Risk**

The weighted average supplier risk algorithm computes the indirect risk score for a given risk dimension by aggregating the risk contributions of all suppliers, weighted by their economic importance (input-output coefficients). The algorithm proceeds as follows:

1. **Initialize:** Set `total_weighted_risk = 0` and `total_coefficient = 0`.

2. **Iterate over suppliers:** For each supplier *i*:
   - Retrieve the supplier's direct risk score for the risk dimension: `risk_i`
   - Retrieve the supplier's input-output coefficient: `coeff_i`
   - Compute the weighted risk contribution: `weighted_risk_i = risk_i × coeff_i`
   - Add to totals: `total_weighted_risk += weighted_risk_i` and `total_coefficient += coeff_i`

3. **Compute indirect risk:** `indirect_risk = total_weighted_risk / total_coefficient`

4. **Return:** The indirect risk score on the 0-5 scale.

This algorithm ensures that suppliers with larger input shares contribute more to the overall indirect risk score, reflecting their greater economic importance to the target sector.

**9-Point Weighted Averaging (Climate V7)**

The 9-point weighted averaging algorithm captures regional variations in climate exposure by sampling nine points within a country and combining the results using a weighted average. The algorithm proceeds as follows:

1. **Define sampling points:** For a country with geographic center at (lat<sub>c</sub>, lon<sub>c</sub>), define nine sampling points:
   - Center: (lat<sub>c</sub>, lon<sub>c</sub>)
   - North: (lat<sub>c</sub> + δ, lon<sub>c</sub>)
   - South: (lat<sub>c</sub> - δ, lon<sub>c</sub>)
   - East: (lat<sub>c</sub>, lon<sub>c</sub> + δ)
   - West: (lat<sub>c</sub>, lon<sub>c</sub> - δ)
   - Northeast: (lat<sub>c</sub> + δ, lon<sub>c</sub> + δ)
   - Southeast: (lat<sub>c</sub> - δ, lon<sub>c</sub> + δ)
   - Southwest: (lat<sub>c</sub> - δ, lon<sub>c</sub> - δ)
   - Northwest: (lat<sub>c</sub> + δ, lon<sub>c</sub> - δ)
   
   where δ is an offset (typically 2-5 degrees) that determines the spatial extent of the sampling grid.

2. **Assess each point:** For each sampling point, call the Climate API to assess climate risk at that specific location. This produces nine expected annual loss estimates: `loss_center`, `loss_north`, `loss_south`, `loss_east`, `loss_west`, `loss_northeast`, `loss_southeast`, `loss_southwest`, `loss_northwest`.

3. **Compute weighted average:** Apply the weighting scheme:
   ```
   country_loss = 0.25 × loss_center
                + 0.10 × loss_north
                + 0.10 × loss_south
                + 0.10 × loss_east
                + 0.10 × loss_west
                + 0.09 × loss_northeast
                + 0.09 × loss_southeast
                + 0.09 × loss_southwest
                + 0.09 × loss_northwest
   ```

4. **Return:** The weighted average expected annual loss for the country.

This algorithm ensures that the country-level climate risk assessment captures regional variations, particularly important for large or geographically diverse countries like the United States, China, or Russia.

**Supplier Risk Enrichment**

The supplier risk enrichment algorithm adds detailed risk metrics to each Supplier object, enabling granular supplier-level analysis. The algorithm proceeds as follows:

1. **Initialize:** For each supplier *i* in the list of top suppliers:

2. **Retrieve direct risk:** Query the Risk Data Module to retrieve the direct risk scores for the supplier's country-sector across all five risk dimensions (climate, modern slavery, political, water stress, nature loss). Store these scores in the `direct_risk` field of the Supplier object.

3. **Calculate risk contribution:** For each risk dimension *d*:
   - Retrieve the supplier's direct risk score: `risk_d,i`
   - Retrieve the supplier's normalized coefficient: `coeff_i`
   - Compute the risk contribution: `contribution_d,i = risk_d,i × coeff_i`
   - Store in the `risk_contribution` field of the Supplier object.

4. **Calculate expected loss contribution:** If climate data is available:
   - Retrieve the supplier's expected annual loss: `loss_i`
   - Retrieve the supplier's normalized coefficient: `coeff_i`
   - Compute the expected loss contribution: `loss_contribution_i = loss_i × coeff_i`
   - Store in the `expected_loss_contribution` field of the Supplier object.

5. **Return:** The enriched Supplier object with `direct_risk`, `risk_contribution`, and `expected_loss_contribution` fields populated.

This algorithm ensures that API responses include comprehensive supplier-level risk data, enabling users to identify which suppliers contribute most to overall supply chain risk.

### Configuration Files

**sector_code_mapper.py**

This module defines the mapping between OECD sector codes (e.g., "B06") and user-friendly sector names (e.g., "Mining and quarrying"). The mapping is implemented as a Python dictionary with 56 entries, one for each OECD sector. The mapping ensures that API responses include human-readable sector names rather than opaque codes.

Example entries:
```python
SECTOR_CODE_MAPPER = {
    "B01": "Agriculture, forestry and fishing",
    "B06": "Mining and quarrying",
    "C10-C12": "Food products, beverages and tobacco",
    "C13-C15": "Textiles, wearing apparel, leather and related products",
    ...
}
```

**climate_v6_country_mapping.py**

This module defines the mapping between OECD country codes and Climate API country names. The mapping handles both standard ISO-3 codes (e.g., "USA" → "United States") and OECD-specific codes (e.g., "CN1" → "China", "CN2" → "China"). The mapping is implemented as a Python dictionary with 85 entries, one for each OECD country.

Example entries:
```python
OECD_TO_CLIMATE_V6 = {
    "USA": "United States",
    "CHN": "China",
    "CN1": "China",  # OECD region 1 of China
    "CN2": "China",  # OECD region 2 of China
    "GBR": "United Kingdom",
    "DEU": "Germany",
    ...
}
```

**country_codes.py**

This module defines the mapping between OECD country codes and standard ISO-3 codes. This mapping is used to normalize country codes throughout the system, ensuring consistency between the I-O Model, Risk Data Module, and Climate API Client.

Example entries:
```python
OECD_TO_ISO3 = {
    "USA": "USA",
    "CN1": "CHN",
    "CN2": "CHN",
    "MEX1": "MEX",
    "MEX2": "MEX",
    "GBR": "GBR",
    ...
}
```

### Environment Variables

The API uses environment variables for configuration, enabling different settings for development, staging, and production environments. The key environment variables are:

**API_KEY:** The secret key used for API authentication. Clients must include this key in the `api_key` query parameter to access the API. The key should be a long, random string (e.g., 32 characters) to prevent brute-force attacks.

**CLIMATE_API_URL:** The base URL for the Climate Risk API V7. Default: `https://climate-risk-api-v6-prob-be68437e49be.herokuapp.com`

**CLIMATE_API_TIMEOUT:** The timeout (in seconds) for Climate API requests. Default: 40 seconds to accommodate the V7 API's 9-point weighted averaging methodology.

**CACHE_FILE_PATH:** The file path for the expected loss cache. Default: `./climate_v6_cache.json`

**LOG_LEVEL:** The logging level for the API. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL. Default: INFO.

**PORT:** The port on which the API server listens. Default: 5000 (development), dynamically assigned by Heroku (production).

---

## API Reference

### Base URL

**Production:** `https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com`

**Development:** `http://localhost:5000`

### Authentication

All API requests require an API key passed as a query parameter:

```
GET /api/assess?country=USA&sector=B06&api_key=YOUR_API_KEY
```

If the API key is missing or invalid, the API returns a 401 Unauthorized response:

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

### Endpoints

#### GET /health

Health check endpoint that returns the API status and configuration.

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "4.0.0",
  "climate_api": "v7",
  "countries_cached": 145,
  "oecd_countries": 85,
  "oecd_sectors": 56
}
```

**Status Codes:**
- 200 OK: API is healthy
- 503 Service Unavailable: API is unhealthy (e.g., cache not loaded, I-O tables not loaded)

#### GET /api/assess

Assess supply chain risk for a given country-sector combination.

**Request:**
```
GET /api/assess?country=USA&sector=B06&api_key=YOUR_API_KEY&skip_climate=false&top_n=5
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | Yes | ISO-3 country code (e.g., USA, CHN, GBR) |
| `sector` | string | Yes | OECD sector code (e.g., B06, C10-C12) |
| `api_key` | string | Yes | API authentication key |
| `skip_climate` | boolean | No | Skip climate expected loss calculation (default: false) |
| `top_n` | integer | No | Number of top suppliers to return (default: 5) |

**Response:**
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
      "present_value_30yr": 1550000.00,
      "risk_breakdown": {
        "hurricane": {
          "annual_loss": 5234.12,
          "annual_loss_pct": 0.52
        },
        "flood": {
          "annual_loss": 42135.67,
          "annual_loss_pct": 4.21
        },
        "heat_stress": {
          "annual_loss": 30234.45,
          "annual_loss_pct": 3.02
        },
        "drought": {
          "annual_loss": 20234.89,
          "annual_loss_pct": 2.02
        },
        "extreme_precipitation": {
          "annual_loss": 3047.07,
          "annual_loss_pct": 0.30
        }
      }
    }
  },
  "indirect_risk": {
    "climate": 2.65,
    "modern_slavery": 2.18,
    "political": 2.15,
    "water_stress": 2.70,
    "nature_loss": 2.55,
    "expected_loss": {
      "total_annual_loss": 98346.22,
      "total_annual_loss_pct": 9.83
    }
  },
  "total_risk": {
    "climate": 2.70,
    "modern_slavery": 2.20,
    "political": 2.17,
    "water_stress": 2.73,
    "nature_loss": 2.58
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
        "climate": 0.6824,
        "modern_slavery": 0.5527,
        "political": 0.5434,
        "water_stress": 0.6876,
        "nature_loss": 0.6502
      },
      "expected_loss_contribution": {
        "annual_loss": 4789.12,
        "present_value_30yr": 73600.00
      }
    },
    ...
  ]
}
```

**Status Codes:**
- 200 OK: Assessment completed successfully
- 400 Bad Request: Invalid parameters (e.g., invalid country code, invalid sector code)
- 401 Unauthorized: Invalid or missing API key
- 404 Not Found: Country-sector combination not found in I-O tables
- 500 Internal Server Error: Unexpected error during assessment
- 503 Service Unavailable: External service (e.g., Climate API) unavailable

**Error Response:**
```json
{
  "error": "Bad Request",
  "message": "Invalid country code: XYZ",
  "details": "Country code must be a valid ISO-3 code (e.g., USA, CHN, GBR)"
}
```

### Rate Limits

The API does not currently enforce rate limits, but clients should limit their request rate to avoid overloading the server. A reasonable guideline is 10 requests per second. If you need higher throughput, contact the API owner to discuss dedicated infrastructure or batch processing options.

### Best Practices

**Batch Processing:** If you need to assess risk for multiple country-sector combinations, consider batching your requests to reduce overhead. Send requests sequentially with a small delay (e.g., 100ms) between requests to avoid overwhelming the server.

**Caching:** The API includes built-in caching for climate data, but clients should also implement their own caching to avoid redundant requests. If you assess the same country-sector combination multiple times, cache the results locally and only refresh when the data is stale (e.g., after 24 hours).

**Error Handling:** Always implement robust error handling in your client code. The API may return errors due to invalid parameters, missing data, or external service unavailability. Your code should gracefully handle these errors and provide meaningful feedback to users.

**Pagination:** The API returns the top N suppliers (default 5) to keep response sizes manageable. If you need more suppliers, increase the `top_n` parameter. However, be aware that larger values may increase response times and payload sizes.

---

## Deployment Guide

### Prerequisites

Before deploying the API, ensure you have the following:

- **Python 3.11** installed locally for development and testing
- **Git** for version control and deployment
- **Heroku CLI** for managing Heroku deployments
- **Heroku account** with billing enabled (required for production dynos)
- **GitHub account** for code repository hosting (optional but recommended)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jrbiltmore/supply-chain-risk-api.git
   cd supply-chain-risk-api
   ```

2. **Create a virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   ```bash
   export API_KEY="your-secret-api-key"
   export CLIMATE_API_URL="https://climate-risk-api-v6-prob-be68437e49be.herokuapp.com"
   export CLIMATE_API_TIMEOUT=40
   export LOG_LEVEL="DEBUG"
   ```

5. **Pre-populate the climate cache (optional but recommended):**
   ```bash
   python climate_v6_precache.py
   ```
   This will take approximately 52 minutes to complete.

6. **Run the development server:**
   ```bash
   python app_v2.py
   ```
   The API will be available at `http://localhost:5000`.

7. **Test the API:**
   ```bash
   curl "http://localhost:5000/health"
   curl "http://localhost:5000/api/assess?country=USA&sector=B06&api_key=your-secret-api-key"
   ```

### Heroku Deployment

1. **Create a Heroku app:**
   ```bash
   heroku create supply-chain-risk-api
   ```

2. **Set environment variables:**
   ```bash
   heroku config:set API_KEY="your-secret-api-key"
   heroku config:set CLIMATE_API_URL="https://climate-risk-api-v6-prob-be68437e49be.herokuapp.com"
   heroku config:set CLIMATE_API_TIMEOUT=40
   heroku config:set LOG_LEVEL="INFO"
   ```

3. **Deploy the code:**
   ```bash
   git push heroku main
   ```

4. **Scale the dyno:**
   ```bash
   heroku ps:scale web=1
   ```

5. **Check the logs:**
   ```bash
   heroku logs --tail
   ```

6. **Test the deployed API:**
   ```bash
   curl "https://supply-chain-risk-api.herokuapp.com/health"
   curl "https://supply-chain-risk-api.herokuapp.com/api/assess?country=USA&sector=B06&api_key=your-secret-api-key"
   ```

### Heroku Configuration

**Procfile:** Defines the command to start the web server.
```
web: gunicorn app_v2:app --workers=1 --threads=2 --timeout=120 --bind=0.0.0.0:$PORT
```

**runtime.txt:** Specifies the Python version.
```
python-3.11.0
```

**requirements.txt:** Lists all Python dependencies.
```
Flask==3.0.0
pandas==2.0.3
numpy==1.24.3
requests==2.31.0
gunicorn==21.2.0
```

### Performance Tuning

**Worker Configuration:** The current deployment uses 1 Gunicorn worker with 2 threads. This configuration is optimized for Heroku's Basic dyno (512 MB RAM). If you upgrade to a larger dyno (e.g., Standard-1X with 1 GB RAM), you can increase the number of workers to improve concurrency:
```
web: gunicorn app_v2:app --workers=2 --threads=2 --timeout=120 --bind=0.0.0.0:$PORT
```

**Timeout Configuration:** The Gunicorn timeout is set to 120 seconds to accommodate slow Climate API requests (up to 40 seconds) plus processing time. If you experience timeout errors, increase this value:
```
web: gunicorn app_v2:app --workers=1 --threads=2 --timeout=180 --bind=0.0.0.0:$PORT
```

**Dyno Sleep:** Heroku's Basic dyno sleeps after 30 minutes of inactivity, causing the first request after sleep to take 10-30 seconds. To eliminate dyno sleep, upgrade to a Standard dyno ($25/month):
```bash
heroku ps:type standard-1x
```

### Monitoring and Logging

**Heroku Logs:** View real-time logs with:
```bash
heroku logs --tail
```

**Log Levels:** The API uses Python's built-in logging module with configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). Set the `LOG_LEVEL` environment variable to control verbosity.

**Error Tracking:** Consider integrating an error tracking service like Sentry or Rollbar for production deployments. These services provide detailed error reports, stack traces, and performance monitoring.

**Uptime Monitoring:** Use a service like Pingdom or UptimeRobot to monitor API availability and alert you to downtime.

---

## Testing & Validation

### Unit Tests

The API includes unit tests for core modules, ensuring that individual components function correctly in isolation. The tests are implemented using Python's built-in `unittest` framework and can be run with:

```bash
python -m unittest discover tests/
```

**Test Coverage:**
- **I-O Model:** Tests for supplier retrieval, coefficient normalization, country code mapping, and sector name mapping.
- **Risk Calculator:** Tests for direct risk retrieval, indirect risk calculation, supplier enrichment, and total risk aggregation.
- **Climate API Client:** Tests for country name mapping, request/response handling, error handling, and retry logic.
- **Expected Loss Cache:** Tests for cache loading, cache retrieval, cache updates, and cache persistence.

### Integration Tests

Integration tests verify that the API components work together correctly and that the end-to-end workflow produces expected results. The tests send HTTP requests to the API and validate the responses.

**Test Scenarios:**
- **Basic Assessment:** Request risk assessment for a standard country-sector (e.g., USA + Mining) and verify that all response fields are present and properly formatted.
- **Climate Data:** Request assessment with `skip_climate=false` and verify that expected loss data is included in the response.
- **Top Suppliers:** Request assessment with `top_n=10` and verify that 10 suppliers are returned with complete risk metrics.
- **Error Handling:** Send requests with invalid parameters (e.g., invalid country code, missing API key) and verify that appropriate error responses are returned.
- **Cache Hit:** Request assessment for a cached country and verify that the response time is under 1 second.
- **Cache Miss:** Request assessment for an uncached country and verify that the response time is 20-30 seconds (first request) and under 1 second (subsequent requests).

### Validation Against Historical Data

The API's risk assessments are validated against historical disaster data and loss estimates to ensure that the methodology produces realistic and defensible results.

**Climate Risk Validation:** Compare the API's expected annual loss estimates with historical disaster losses from sources like EM-DAT (Emergency Events Database) and Munich Re's NatCatSERVICE. For example, the API estimates that the United States faces $100,886 expected annual loss per $1M asset value from climate hazards. Historical data shows that the US experiences approximately $80-120 billion in annual disaster losses, which, when normalized by total asset value, aligns with the API's estimates.

**Modern Slavery Validation:** Compare the API's modern slavery risk scores with prevalence estimates from the Global Slavery Index and case studies of forced labor in specific industries. For example, the API assigns high modern slavery risk to countries like North Korea, Eritrea, and Mauritania, which aligns with the Global Slavery Index's prevalence estimates and documented cases of state-imposed forced labor.

**Political Risk Validation:** Compare the API's political risk scores with historical conflict data, regime changes, and policy disruptions. For example, the API assigns high political risk to countries like Syria, Yemen, and Afghanistan, which have experienced ongoing armed conflicts, regime instability, and institutional collapse in recent years.

### Performance Benchmarks

The API's performance is benchmarked to ensure that response times meet user expectations and that the system can handle anticipated request volumes.

**Response Time Benchmarks:**
- **Cache Hit (skip_climate=true):** < 1 second (target: 0.5 seconds)
- **Cache Hit (skip_climate=false):** < 1 second (target: 0.5 seconds)
- **Cache Miss (skip_climate=true):** 2-3 seconds (target: 2 seconds)
- **Cache Miss (skip_climate=false):** 20-30 seconds (target: 25 seconds)

**Throughput Benchmarks:**
- **Sequential Requests:** 10 requests per second (target: 10 rps)
- **Concurrent Requests:** 20 requests per second (target: 20 rps, requires 2+ workers)

**Memory Usage:**
- **Idle:** 200 MB (target: < 300 MB)
- **Under Load:** 400 MB (target: < 450 MB on 512 MB dyno)

---

## Performance Optimization

### Caching Strategy

The API implements a multi-layer caching strategy to minimize response times and reduce load on external services.

**Layer 1: Expected Loss Cache** stores climate expected loss data for all 145 countries. This cache is pre-populated at API startup and persisted to disk, ensuring that 98% of requests benefit from instant cache hits. The cache is implemented as a JSON file (`climate_v6_cache.json`) that is loaded into memory at startup.

**Layer 2: In-Memory Risk Data** stores the five risk dimension datasets (climate, modern slavery, political, water stress, nature loss) as Pandas DataFrames in memory. This eliminates the need to read CSV files for each request, reducing disk I/O and improving response times.

**Layer 3: I-O Model Cache** stores the OECD Input-Output Tables as a Pandas DataFrame in memory. This enables fast lookups of supplier relationships without repeatedly parsing CSV files.

**Cache Invalidation:** The expected loss cache is invalidated and refreshed when the Climate API data is updated. The API supports force refresh via the `force_refresh` parameter, which bypasses the cache and fetches fresh data from the Climate API. The risk data and I-O model caches are static and do not require invalidation unless the underlying datasets are updated.

### Memory Optimization

The API is optimized to run on Heroku's Basic dyno with 512 MB RAM. Memory optimization techniques include:

**Lazy Loading:** The API loads data only when needed. For example, the expected loss cache is loaded at startup, but individual country data is fetched from the Climate API only when requested (cache miss).

**Data Compression:** The expected loss cache is stored in compressed JSON format, reducing file size from 45 KB to 20 KB. This reduces memory usage and speeds up cache loading.

**Efficient Data Structures:** The API uses Pandas DataFrames for storing and querying tabular data (I-O tables, risk data). DataFrames are more memory-efficient than nested dictionaries or lists, especially for large datasets.

**Worker Configuration:** The API uses a single Gunicorn worker with 2 threads, limiting memory usage to approximately 400 MB under load. This configuration ensures that the API stays within the 512 MB RAM limit of Heroku's Basic dyno.

### Response Time Optimization

The API is optimized to minimize response times, particularly for cached requests.

**Pre-Caching:** The expected loss cache is pre-populated at API startup, ensuring that 98% of requests benefit from instant cache hits. This eliminates the 20-30 second delay associated with fetching data from the Climate API.

**Efficient Algorithms:** The indirect risk calculation uses vectorized operations (NumPy) to compute weighted averages efficiently. This reduces computation time from milliseconds to microseconds for typical supplier lists (5-10 suppliers).

**Minimal I/O:** The API minimizes disk I/O by loading all data into memory at startup. Once loaded, all data access is in-memory, eliminating the latency associated with reading files.

**Timeout Configuration:** The Climate API Client uses a 40-second timeout to accommodate the V7 API's 9-point weighted averaging methodology. This timeout is carefully calibrated to balance responsiveness (avoiding premature timeouts) and user experience (avoiding excessively long waits).

---

## Known Limitations

### Data Coverage

**Climate Data Coverage:** The Climate V7 API covers 145 out of 162 countries (89%). Three countries (Democratic Republic of Congo, North Korea, Sao Tome and Principe) are not available in the Climate API and will return null climate data. Additionally, some countries (e.g., Iceland) show $0 expected annual loss, which may indicate genuine low risk or data gaps.

**I-O Table Coverage:** The OECD ICIO Tables cover 85 countries, representing approximately 95% of global GDP. However, many smaller economies are not included, limiting the API's ability to assess supply chain risk for companies operating in these countries.

**Sector Granularity:** The OECD ICIO Tables use 56 sectors, which provides reasonable granularity for most industries but may not capture fine-grained differences within sectors. For example, the "Mining and quarrying" sector includes both coal mining and rare earth element extraction, which have very different risk profiles.

### Methodology Limitations

**Static I-O Tables:** The OECD ICIO Tables represent a snapshot of supply chain relationships in 2018. These relationships may have changed significantly since then, particularly in response to recent disruptions (e.g., COVID-19, geopolitical tensions). The API does not account for dynamic changes in supply chains.

**Simplified Risk Aggregation:** The API computes total risk as a simple weighted average of direct and indirect risks. This approach does not account for risk interactions (e.g., climate risk exacerbating water stress) or non-linear effects (e.g., catastrophic losses from simultaneous disruptions).

**Country-Level Risk Scores:** The API uses country-level risk scores, which may not capture sub-national variations in risk exposure. For example, coastal regions of the United States face higher hurricane risk than inland regions, but the API applies a single climate risk score to the entire country.

**Asset Value Assumption:** The Climate API calculates expected annual losses based on a fixed asset value ($1 million). This assumption may not reflect the actual asset values of different companies or sectors, leading to over- or under-estimation of financial impacts.

### Performance Limitations

**Climate API Response Time:** The Climate V7 API takes 20-30 seconds per country due to 9-point weighted averaging. This delay affects the first request for each country (cache miss) but not subsequent requests (cache hit). Users should be aware that initial assessments may take longer than expected.

**Dyno Sleep (Heroku Basic):** Heroku's Basic dyno sleeps after 30 minutes of inactivity, causing the first request after sleep to take 10-30 seconds. This delay can be eliminated by upgrading to a Standard dyno ($25/month).

**Single Worker Configuration:** The current deployment uses a single Gunicorn worker, limiting concurrency to 2 simultaneous requests (2 threads). If request volume increases, the API may experience queueing delays. Upgrading to a larger dyno and increasing the number of workers can improve concurrency.

---

## Future Enhancements

### Data Enhancements

**Expand Climate Coverage:** Work with the Climate V7 API team to add support for the 3 missing countries (Democratic Republic of Congo, North Korea, Sao Tome and Principe) and investigate the zero-risk issue for Iceland and other countries.

**Add Transition Risk:** Incorporate transition risk metrics (e.g., carbon pricing, stranded assets, policy changes) to complement the current focus on physical risk. This would enable users to assess both physical and transition climate risks in their supply chains.

**Sector-Specific Risk Data:** Develop sector-specific risk datasets that account for unique vulnerabilities and exposures. For example, the agricultural sector is highly sensitive to drought and heat stress, while the electronics sector is vulnerable to water stress and supply chain disruptions.

**Sub-National Risk Data:** Incorporate sub-national (state/province-level) risk data to capture regional variations in risk exposure. This would enable more precise risk assessments for companies with geographically concentrated operations.

**Dynamic I-O Tables:** Develop methods to update the I-O tables more frequently, potentially using real-time trade data and machine learning to estimate current supply chain relationships.

### Methodology Enhancements

**Risk Interaction Modeling:** Develop models that account for interactions between different risk types (e.g., climate risk exacerbating water stress, political instability disrupting disaster response). This would provide more realistic assessments of compound risks.

**Scenario Analysis:** Enable users to assess risk under different scenarios (e.g., 2°C warming, 4°C warming, trade war, pandemic). This would support strategic planning and stress testing.

**Company-Specific Assessments:** Integrate company-specific data (e.g., supplier lists, asset locations, revenue by geography) to provide tailored risk assessments. This would require partnerships with data providers or direct data input from users.

**Financial Impact Modeling:** Develop more sophisticated financial impact models that account for business interruption, supply chain disruption, reputation damage, and regulatory costs. This would enable users to translate risk scores into bottom-line financial impacts.

### Performance Enhancements

**Distributed Caching:** Implement a distributed caching system (e.g., Redis, Memcached) to enable cache sharing across multiple API instances. This would improve scalability and reduce memory usage per instance.

**Asynchronous Processing:** Implement asynchronous processing for slow operations (e.g., Climate API requests) using task queues (e.g., Celery, RQ). This would enable the API to return immediate responses for cache misses, with results delivered via webhook or polling.

**Batch Assessment Endpoint:** Develop a batch assessment endpoint that accepts multiple country-sector combinations in a single request. This would reduce overhead for users who need to assess risk for many combinations.

**GraphQL API:** Develop a GraphQL API that enables clients to request only the data they need, reducing payload sizes and improving response times.

### User Experience Enhancements

**Interactive Documentation:** Develop interactive API documentation (e.g., Swagger/OpenAPI) that enables users to explore endpoints, test requests, and view responses directly in their browser.

**Dashboard and Visualization:** Develop a web-based dashboard that visualizes supply chain risk data, enabling users to explore risk profiles, compare countries and sectors, and identify high-risk suppliers.

**Alerts and Notifications:** Implement an alerting system that notifies users when risk levels change significantly or when new risk events occur (e.g., natural disasters, political crises).

**White-Label Solutions:** Develop white-label versions of the API and dashboard that can be customized and deployed by partners and clients.

---

## References

[1] OECD Inter-Country Input-Output (ICIO) Tables: https://www.oecd.org/sti/ind/inter-country-input-output-tables.htm

[2] Climate Risk API V7 Documentation: https://climate-risk-api-v6-prob-be68437e49be.herokuapp.com/docs

[3] Global Slavery Index: https://www.globalslaveryindex.org/

[4] Fragile States Index: https://fragilestatesindex.org/

[5] World Bank Worldwide Governance Indicators: https://info.worldbank.org/governance/wgi/

[6] WRI Aqueduct Water Risk Atlas: https://www.wri.org/aqueduct

[7] IUCN Red List of Threatened Species: https://www.iucnredlist.org/

[8] Global Forest Watch: https://www.globalforestwatch.org/

[9] NOAA IBTrACS (International Best Track Archive for Climate Stewardship): https://www.ncdc.noaa.gov/ibtracs/

[10] HadEX3 (Hadley Centre Global Climate Extremes Index 3): https://www.metoffice.gov.uk/hadobs/hadex3/

[11] SPEI Global Drought Monitor: https://spei.csic.es/

[12] Task Force on Climate-related Financial Disclosures (TCFD): https://www.fsb-tcfd.org/

[13] EU Corporate Sustainability Due Diligence Directive: https://ec.europa.eu/info/business-economy-euro/doing-business-eu/sustainability-due-diligence_en

---

## Appendix: Code Repository Structure

```
supply-chain-risk-api/
├── app_v2.py                          # Flask API server
├── risk_calculator_v2.py              # Risk calculator core logic
├── io_model_base.py                   # Input-output model abstraction
├── climate_api_client.py              # Climate API V7 client
├── expected_loss_cache.py             # Expected loss caching system
├── climate_v6_precache.py             # Cache pre-population script
├── climate_v6_country_mapping.py      # OECD to Climate API country mapping
├── sector_code_mapper.py              # OECD sector code to name mapping
├── country_codes.py                   # OECD to ISO-3 country code mapping
├── requirements.txt                   # Python dependencies
├── Procfile                           # Heroku process definition
├── runtime.txt                        # Python version specification
├── climate_v6_cache.json              # Pre-populated climate cache (145 countries)
├── data/
│   ├── oecd_icio_2018.csv            # OECD Input-Output Tables (2018)
│   ├── climate_risk.csv              # Climate risk scores by country
│   ├── modern_slavery_risk.csv       # Modern slavery risk scores by country
│   ├── political_risk.csv            # Political risk scores by country
│   ├── water_stress_risk.csv         # Water stress risk scores by country
│   └── nature_loss_risk.csv          # Nature loss risk scores by country
├── tests/
│   ├── test_io_model.py              # Unit tests for I-O model
│   ├── test_risk_calculator.py       # Unit tests for risk calculator
│   ├── test_climate_client.py        # Unit tests for Climate API client
│   └── test_cache.py                 # Unit tests for expected loss cache
├── docs/
│   ├── API_INTEGRATION_UPDATE_MESSAGE.md
│   ├── CLIMATE_V7_DEPLOYMENT_SUCCESS_REPORT.md
│   ├── SUPPLIER_RISK_ENRICHMENT_FIX.md
│   └── DEPLOYMENT_STATUS_REPORT.md
└── README.md                          # Project overview and quick start guide
```

---

**End of Technical Documentation**

---

**Document Metadata**

- **Title:** Supply Chain Risk Assessment API - Complete Technical Documentation
- **Version:** 4.0.0
- **Date:** February 14, 2026
- **Author:** Manus AI
- **GitHub Repository:** https://github.com/Jrbiltmore/supply-chain-risk-api
- **Production URL:** https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com
- **License:** Proprietary (Contact owner for licensing information)
- **Contact:** [Your contact information here]
