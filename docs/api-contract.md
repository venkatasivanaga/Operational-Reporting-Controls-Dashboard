# API contract (initial)

## Auth
- `POST /auth/login` -> { access_token, token_type, user }
- `GET /auth/me` -> current user

## Controls
- `GET /controls` (filters + pagination)
- `POST /controls` (admin)
- `GET /controls/{id}`
- `PUT /controls/{id}` (admin)
- `DELETE /controls/{id}` (admin)

## Incidents
- `GET /incidents` (filters + pagination)
- `POST /incidents` (admin)
- `GET /incidents/{id}`
- `PUT /incidents/{id}` (admin)
- `DELETE /incidents/{id}` (admin)

## Tests
- `GET /tests` (filters + pagination)
- `POST /tests` (admin)
- `GET /tests/{id}`
- `PUT /tests/{id}` (admin)
- `DELETE /tests/{id}` (admin)

## Metrics
- `GET /metrics/summary`
  - open_incidents
  - pass_rate
  - mttr_hours
  - trends: incidents_over_time, pass_rate_over_time
