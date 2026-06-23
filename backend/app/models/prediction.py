from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.competitor import Competitor


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    competitor_id: Mapped[int] = mapped_column(Integer, ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String(1024), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    target_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=True) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)


    competitor: Mapped["Competitor"] = relationship("Competitor", back_populates="predictions")
