from datetime import datetime
from pydantic import BaseModel, Field


class ControlBase(BaseModel):
    control_code: str = Field(..., max_length=50, examples=["OPS-CTRL-001"])
    title: str = Field(..., max_length=200)
    description: str = ""
    owner: str = Field(..., max_length=120)
    frequency: str = "monthly"
    risk_rating: str = "medium"
    status: str = "active"


class ControlCreate(ControlBase):
    pass


class ControlUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    owner: str | None = Field(default=None, max_length=120)
    frequency: str | None = None
    risk_rating: str | None = None
    status: str | None = None


class ControlOut(ControlBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
