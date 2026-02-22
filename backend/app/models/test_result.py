from datetime import date
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from backend.app.db.base import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    control_id: Mapped[int] = mapped_column(ForeignKey("controls.id", ondelete="CASCADE"), index=True)

    test_date: Mapped[date] = mapped_column(Date, default=date.today)
    result: Mapped[str] = mapped_column(String(10), default="pass")  # pass/fail
    evidence_url: Mapped[str] = mapped_column(String(500), default="")
    notes: Mapped[str] = mapped_column(String(2000), default="")

    control = relationship("Control", back_populates="test_results")
