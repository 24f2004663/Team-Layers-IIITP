from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, JSON
from app.models.base import Base

class IdentityProfile(Base):
    """User personality mapping and growth archetype profile model."""
    __tablename__ = "identity_profiles"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    archetype: Mapped[str] = mapped_column(String(100), default="Explorer", nullable=False)
    core_values: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    strengths: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    weaknesses: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="identity_profile")
