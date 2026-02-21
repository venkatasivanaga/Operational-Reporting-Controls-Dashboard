# Operational Reporting Controls Dashboard

A full-stack dashboard for **operational reporting**, **control monitoring**, and **incident tracking** — designed to look like a lightweight internal tool used by Ops / Compliance / Reliability teams.

## Problem this solves
Teams often track controls, incidents, and testing evidence across spreadsheets and ad-hoc docs. This project provides a single dashboard to:
- monitor operational KPIs,
- track control health and testing outcomes,
- connect incidents to services and owners,
- quickly generate a “ready-for-audit” view of control evidence.

## Users & roles
- **Viewer**: read-only access to dashboards and records
- **Admin**: can create/update/delete records (controls, incidents, tests)

## Core data model
- **Controls**: operational/compliance controls (owner, frequency, risk, status)
- **Incidents**: events that impact operations (severity, service, status, timestamps)
- **Control Tests**: test results linked to controls (pass/fail, date, evidence URL)

## MVP scope
### Backend (API + DB)
- FastAPI REST API with validation and pagination
- SQLite for local development (optional Postgres for deployment)
- Auth-lite (JWT) with demo users
- CRUD endpoints:
  - Controls
  - Incidents
  - Control Tests
- Metrics endpoint:
  - open incidents
  - control test pass rate
  - MTTR (mean time to resolution)
  - basic trends over time

### Frontend (Dashboard UI)
- Minimal, classic UI (clean layout, readable typography)
- Login + route protection
- Dashboard page:
  - KPI cards
  - trend charts
- Data views:
  - filterable tables (controls/incidents/tests)
  - record detail view / drawer
  - admin-only create/edit actions

## Stretch features
- Role-based UI gating (Viewer vs Admin)
- Audit log (who changed what, when)
- Export reporting (CSV export, monthly summary view)

## Non-goals (for this project)
- Complex SSO or enterprise identity integration
- Multi-tenant organizations
- Real-time streaming updates (WebSockets)

## Local development (planned)
- `backend/` runs FastAPI on `http://localhost:8000`
- `frontend/` runs Vite on `http://localhost:5173`
- Frontend calls backend via `VITE_API_BASE_URL`

## Deployment (planned)
- Backend: Render (FastAPI + Postgres)
- Frontend: Vercel (or GitHub Pages)