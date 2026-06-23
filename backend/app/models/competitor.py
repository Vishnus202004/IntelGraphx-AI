from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Boolean, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.hash import Hash
    from app.models.alert import Alert
    from app.models.prediction import Prediction


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    pricing_url: Mapped[str] = mapped_column(String(512), nullable=True)
    blog_url: Mapped[str] = mapped_column(String(512), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    # Relationships
    hashes: Mapped[List["Hash"]] = relationship("Hash", back_populates="competitor", cascade="all, delete-orphan")
    alerts: Mapped[List["Alert"]] = relationship("Alert", back_populates="competitor", cascade="all, delete-orphan")
    predictions: Mapped[List["Prediction"]] = relationship("Prediction", back_populates="competitor", cascade="all, delete-orphan")
