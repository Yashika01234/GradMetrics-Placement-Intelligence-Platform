# GradMetrics — Placement Intelligence Platform

A polished local analytics dashboard for a fictional engineering institute. It analyzes placement outcomes by branch and cohort, salary/package statistics, student outcomes, historical trends, explainable forecasts, and what-if placement scenarios.

> **Important:** All 2,000+ student records in this project are synthetic demo data. The institution and company names are fictional. Do not present these numbers as official statistics for any real college.

## Run on Windows — no package installation

1. Extract this ZIP.
2. Open the `GradMetrics_Placement_Intelligence` folder in VS Code.
3. Open Terminal → New Terminal.
4. Run `py run.py`.
5. Open **http://127.0.0.1:8000** in your browser.

Or double-click `run.bat`.

**No pip install is required.** Backend uses only Python's standard library. No Streamlit, Uvicorn, FastAPI, Pydantic, Node or virtual environment required.

## Features
- Executive KPIs: total students, placed students, placement rate, average/median/highest package.
- Branch comparison across Computer Science, IT, Electronics & Communication, Electrical, Mechanical, and Instrumentation & Control.
- Searchable anonymized student outcomes with CGPA, company, status and package.
- Year and branch filters.
- Forecast studio using ordinary least-squares linear regression on yearly placement percentages. This is a transparent illustrative baseline, not a reliable prediction.
- What-if simulator to estimate how additional placements change the placement percentage.
- CSV export of filtered student records.
- JSON API endpoints.

## Architecture
- `server.py` — standard-library HTTP server, CSV data access, filtering, metrics, regression forecast and scenario API.
- `static/index.html` — dashboard structure.
- `static/styles.css` — responsive interface styling.
- `static/app.js` — charts, filters, tables, API calls, simulator and CSV export.
- `data/students.csv` — synthetic student-level data.

## API
- `GET /api/summary?year=All&branch=All`
- `GET /api/students?year=All&branch=All`
- `GET /api/forecast`
- `POST /api/scenario` with JSON: `{"current_placed":500,"total_students":700,"additional_placements":25}`

## Honest limitations
This is a portfolio-grade analytics prototype, not a production placement-management system. It has no authentication, role permissions, persistent database, or validated CSV upload yet. The forecast uses only three synthetic cohorts and should not be used for real institutional planning.

## Good next extensions
PostgreSQL persistence, placement officer/student roles, validated CSV ingestion, audit logs, automated tests, and a properly evaluated ML model trained on authorized historical placement data.
