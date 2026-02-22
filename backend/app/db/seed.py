from datetime import datetime, timedelta, date

from backend.app.db.session import SessionLocal
from backend.app.models.control import Control
from backend.app.models.incident import Incident
from backend.app.models.test_result import TestResult


def seed() -> None:
    db = SessionLocal()
    try:
        # Controls
        controls = [
            {
                "control_code": "OPS-CTRL-001",
                "title": "Daily backup verification",
                "description": "Verify backups completed successfully and are recoverable.",
                "owner": "Ops Team",
                "frequency": "daily",
                "risk_rating": "high",
                "status": "active",
            },
            {
                "control_code": "OPS-CTRL-002",
                "title": "Weekly access review",
                "description": "Review access changes for privileged roles and validate approvals.",
                "owner": "Security",
                "frequency": "weekly",
                "risk_rating": "high",
                "status": "active",
            },
            {
                "control_code": "OPS-CTRL-003",
                "title": "Monthly incident postmortems",
                "description": "Ensure Sev1/Sev2 incidents have a documented RCA and action items.",
                "owner": "SRE",
                "frequency": "monthly",
                "risk_rating": "medium",
                "status": "active",
            },
        ]

        for c in controls:
            exists = db.query(Control).filter(Control.control_code == c["control_code"]).first()
            if not exists:
                db.add(Control(**c))

        db.commit()

        # Map controls by code to ids
        ctrl_map = {c.control_code: c.id for c in db.query(Control).all()}

        # Incidents
        now = datetime.utcnow()
        incidents = [
            {
                "incident_code": "INC-2026-0001",
                "title": "API latency spike",
                "service": "controls-api",
                "severity": "sev2",
                "status": "open",
                "owner": "SRE",
                "notes": "Investigating elevated p95 latency.",
                "opened_at": now - timedelta(hours=3),
                "resolved_at": None,
            },
            {
                "incident_code": "INC-2026-0002",
                "title": "Backup job failure",
                "service": "backup-scheduler",
                "severity": "sev3",
                "status": "resolved",
                "owner": "Ops Team",
                "notes": "Transient storage issue; rerun succeeded.",
                "opened_at": now - timedelta(days=2, hours=5),
                "resolved_at": now - timedelta(days=2, hours=2),
            },
        ]

        for i in incidents:
            exists = db.query(Incident).filter(Incident.incident_code == i["incident_code"]).first()
            if not exists:
                db.add(Incident(**i))

        db.commit()

        # Test Results
        tests = [
            {
                "control_id": ctrl_map.get("OPS-CTRL-001"),
                "test_date": date.today(),
                "result": "fail",
                "evidence_url": "https://example.com/evidence/ops-ctrl-001",
                "notes": "Backup job failed on node-3; rerun scheduled.",
            },
            {
                "control_id": ctrl_map.get("OPS-CTRL-002"),
                "test_date": date.today() - timedelta(days=7),
                "result": "pass",
                "evidence_url": "https://example.com/evidence/ops-ctrl-002",
                "notes": "Access changes reviewed and approved.",
            },
        ]

        for t in tests:
            if not t["control_id"]:
                continue
            # prevent duplicates by (control_id, test_date, result)
            exists = (
                db.query(TestResult)
                .filter(
                    TestResult.control_id == t["control_id"],
                    TestResult.test_date == t["test_date"],
                    TestResult.result == t["result"],
                )
                .first()
            )
            if not exists:
                db.add(TestResult(**t))

        db.commit()
        print("Seed complete ?")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
