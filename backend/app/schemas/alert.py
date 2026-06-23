from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    competitor_id: int
    severity: str = "GREEN"  # GREEN, YELLOW, RED
    title: str
    description: str
    is_approved: bool = False


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    severity: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_approved: Optional[bool] = None


class AlertInDBBase(AlertBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Alert(AlertInDBBase):
    pass
