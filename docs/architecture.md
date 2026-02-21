# Architecture

## Overview
This project is a lightweight internal-style dashboard that tracks:
- Controls
- Incidents
- Control test results (evidence)

It is split into a backend API and a frontend SPA.

## Components
- **Frontend (React + TS)**:
  - Auth flow (login, token storage)
  - Dashboard KPIs + trends
  - Tables and detail views (Controls/Incidents/Tests)
- **Backend (FastAPI)**:
  - JWT auth (demo users)
  - REST CRUD endpoints
  - Metrics aggregation endpoint
- **Database (SQLite dev / Postgres prod)**:
  - Controls, Incidents, Test Results, Users (and optional Audit Log)

## Request flow
1. User logs in on frontend
2. Frontend calls `POST /auth/login`
3. Backend returns JWT access token
4. Frontend stores token and attaches it to requests
5. Backend validates token and enforces role permissions
6. Frontend renders KPIs/tables from API responses

## Environments
- Local dev: FastAPI `:8000`, Vite `:5173`
- Prod: Backend on Render, frontend on Vercel (or GitHub Pages)
