from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.competitor import Competitor
from app.schemas.competitor import CompetitorCreate, CompetitorInDBBase

router = APIRouter()

@router.get("/", response_model=List[CompetitorInDBBase])
async def read_competitors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).offset(skip).limit(limit))
    competitors = result.scalars().all()
    return competitors

@router.post("/", response_model=CompetitorInDBBase, status_code=status.HTTP_201_CREATED)
async def create_competitor(competitor_in: CompetitorCreate, db: AsyncSession = Depends(get_db)):
    db_competitor = Competitor(**competitor_in.model_dump())
    db.add(db_competitor)
    await db.commit()
    await db.refresh(db_competitor)
    return db_competitor

@router.delete("/{competitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competitor(competitor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    await db.delete(competitor)
    await db.commit()
    return None
