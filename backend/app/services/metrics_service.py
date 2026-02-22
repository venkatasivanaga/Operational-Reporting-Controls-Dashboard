from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models.incident import Incident
from backend.app.models.test_result import TestResult


def compute_metrics(db: Session) -> dict:
    # Open incidents
    open_incidents = db.query(func.count(Incident.id)).filter(Incident.status != "resolved").scalar() or 0

    # Incidents by status
    incidents_by_status_rows = (
        db.query(Incident.status, func.count(Incident.id))
        .group_by(Incident.status)
        .all()
    )
    incidents_by_status = {status: count for status, count in incidents_by_status_rows}

    # Tests by result
    tests_by_result_rows = (
        db.query(TestResult.result, func.count(TestResult.id))
        .group_by(TestResult.result)
        .all()
    )
    tests_by_result = {result: count for result, count in tests_by_result_rows}

    total_tests = sum(tests_by_result.values())
    passed_tests = tests_by_result.get("pass", 0)
    pass_rate = (passed_tests / total_tests) if total_tests > 0 else None

    # MTTR (Mean Time To Resolution) in hours for resolved incidents
    # Only consider incidents that have resolved_at and opened_at
    mttr_query = (
        db.query(func.avg(func.strftime('%s', Incident.resolved_at) - func.strftime('%s', Incident.opened_at)))
        .filter(Incident.resolved_at.isnot(None))
    )
    avg_seconds = mttr_query.scalar()
    mttr_hours = (avg_seconds / 3600.0) if avg_seconds is not None else None

    return {
        "open_incidents": open_incidents,
        "pass_rate": pass_rate,
        "mttr_hours": mttr_hours,
        "incidents_by_status": incidents_by_status,
        "tests_by_result": tests_by_result,
    }
