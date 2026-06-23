from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionInDBBase

router = APIRouter()

@router.get("/", response_model=List[PredictionInDBBase])
async def read_predictions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve the AI generated strategic forecasts for competitors.
    """
    result = await db.execute(select(Prediction).order_by(Prediction.created_at.desc()).offset(skip).limit(limit))
    predictions = result.scalars().all()
    return predictions
