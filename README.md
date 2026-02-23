# Operational Reporting Controls Dashboard

A full-stack dashboard that mirrors how Ops / Compliance / Reliability teams track **controls**, **incidents**, and **testing evidence** — plus a KPI view for operational health (open incidents, pass rate, MTTR).

This is a portfolio project designed to look like a lightweight internal tool: clean UI, documented API, reproducible demo data.

## Features

### Backend (FastAPI)
- CRUD APIs for:
  - **Controls**
  - **Incidents**
  - **Control Tests** (linked to controls)
- **Metrics endpoint** (`/api/metrics/summary`)
  - open incidents
  - pass rate
  - MTTR (mean time to resolution)
  - breakdowns by status/result
- SQLite for local dev + Alembic migrations
- Demo seed script for realistic sample data

### Frontend (React + TypeScript)
- Minimal dashboard UI
- Fetches live KPIs from the backend metrics endpoint
- Tailwind CSS styling

## Local setup

### 1) Backend
```bash
conda create -n orcd python=3.11 -y
conda activate orcd
python -m pip install -r backend/requirements.txt
conda run -n orcd uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: `http://127.0.0.1:8000/docs`

(Optional) Load demo data:
```bash
conda run -n orcd python -m backend.app.db.seed
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

Create `frontend/.env.local`:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

> **Windows note:** if PowerShell blocks `npm` scripts, use:
> - `npm.cmd install`
> - `npm.cmd run dev`

## Key endpoints
- `GET /api/controls`
- `GET /api/incidents`
- `GET /api/tests`
- `GET /api/metrics/summary`

## Why this project matters
Operational reporting often ends up in spreadsheets. This project demonstrates how to:
- model controls/incidents/tests in a clean schema,
- expose stable APIs with validation and metrics,
- and build a UI that reads from real endpoints.

## Roadmap
- Tables pages for Controls / Incidents / Tests (filters + detail views)
- Role-based access (Viewer vs Admin)
- Audit logging
- CSV export / monthly reporting

## License
MIT
