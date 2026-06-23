from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


class CompetitorBase(BaseModel):
    name: str
    domain: str
    pricing_url: Optional[str] = None
    blog_url: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: bool = True


class CompetitorCreate(CompetitorBase):
    pass


class CompetitorUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    pricing_url: Optional[str] = None
    blog_url: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None


class CompetitorInDBBase(CompetitorBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Competitor(CompetitorInDBBase):
    pass
