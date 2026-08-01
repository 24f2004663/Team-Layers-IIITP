from typing import Any, Dict, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, JSON
from app.models.base import Base

class DailyPlan(Base):
    """Daily schedule, focus time allocations, and short-term task plans model."""
    __tablename__ = "daily_plans"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tasks: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    focus_time_slots: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="daily_plans")
