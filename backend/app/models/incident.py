from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    incident_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    service: Mapped[str] = mapped_column(String(120), default="unknown")
    severity: Mapped[str] = mapped_column(String(10), default="sev3")
    status: Mapped[str] = mapped_column(String(20), default="open")
    owner: Mapped[str] = mapped_column(String(120), default="unassigned")
    notes: Mapped[str] = mapped_column(String(2000), default="")

    opened_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
