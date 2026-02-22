from datetime import datetime
from pydantic import BaseModel, Field


class IncidentBase(BaseModel):
    incident_code: str = Field(..., max_length=50, examples=["INC-2026-0001"])
    title: str = Field(..., max_length=200)
    service: str = "unknown"
    severity: str = "sev3"
    status: str = "open"
    owner: str = "unassigned"
    notes: str = ""


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    service: str | None = None
    severity: str | None = None
    status: str | None = None
    owner: str | None = None
    notes: str | None = None
    resolved_at: datetime | None = None


class IncidentOut(IncidentBase):
    id: int
    opened_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True
