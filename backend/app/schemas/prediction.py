from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class PredictionBase(BaseModel):
    competitor_id: int
    title: str
    content: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    target_date: Optional[datetime] = None
    is_correct: Optional[bool] = None


class PredictionCreate(PredictionBase):
    pass


class PredictionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    target_date: Optional[datetime] = None
    is_correct: Optional[bool] = None


class PredictionInDBBase(PredictionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Prediction(PredictionInDBBase):
    pass
