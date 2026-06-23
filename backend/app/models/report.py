from datetime import datetime
from sqlalchemy import String, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(4096), nullable=False)  # Long executive summaries
    file_path: Mapped[str] = mapped_column(String(512), nullable=True)  # PDF file location
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Timestamp of email delivery
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
