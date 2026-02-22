from datetime import date
from pydantic import BaseModel, Field


class TestResultBase(BaseModel):
    control_id: int
    test_date: date = Field(default_factory=date.today)
    result: str = "pass"  # pass/fail
    evidence_url: str = ""
    notes: str = ""


class TestResultCreate(TestResultBase):
    pass


class TestResultUpdate(BaseModel):
    test_date: date | None = None
    result: str | None = None
    evidence_url: str | None = None
    notes: str | None = None


class TestResultOut(TestResultBase):
    id: int

    class Config:
        from_attributes = True
