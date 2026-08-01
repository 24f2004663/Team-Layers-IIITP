from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime
from app.models.base import Base

class Goal(Base):
    """User goals and milestones model."""
    __tablename__ = "goals"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_long_term: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    target_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="goals")
