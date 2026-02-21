# Data model

## Entities (high level)

### User
- id (uuid/int)
- email
- name
- role: `viewer | admin`
- password_hash

### Control
- id
- control_code (e.g., OPS-CTRL-001)
- title
- description
- owner
- frequency (daily/weekly/monthly/quarterly)
- risk_rating (low/medium/high)
- status (active/paused/deprecated)
- created_at, updated_at

### Incident
- id
- incident_code (e.g., INC-2026-0001)
- title
- service
- severity (sev1-sev4)
- status (open/mitigated/resolved)
- opened_at
- resolved_at (nullable)
- owner
- notes (nullable)

### TestResult
- id
- control_id (FK -> Control)
- test_date
- result (pass/fail)
- evidence_url (nullable)
- notes (nullable)

## Relationships
- Control 1 --- * TestResult
- User (admin) can create/update/delete records (authorization only; not necessarily FK ownership)

## Metric definitions (MVP)
- Open incidents: incidents where status != resolved
- Pass rate: passed tests / total tests (optional time window)
- MTTR: avg(resolved_at - opened_at) for resolved incidents
