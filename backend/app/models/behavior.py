from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from app.models.base import Base

class BehaviorProfile(Base):
    """User behavioral logging and habit streaks model."""
    __tablename__ = "behavior_profiles"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    habits: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    cognitive_patterns: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    energy_levels: Mapped[Dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="behavior_profile")
