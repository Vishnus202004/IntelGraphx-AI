from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    title: str
    summary: str
    file_path: Optional[str] = None
    sent_at: Optional[datetime] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    file_path: Optional[str] = None
    sent_at: Optional[datetime] = None


class ReportInDBBase(ReportBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Report(ReportInDBBase):
    pass
