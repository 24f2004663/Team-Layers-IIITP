from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, Boolean
from app.models.base import Base

class Recommendation(Base):
    """User recommendations linking to target resources model."""
    __tablename__ = "recommendations"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    resource_id: Mapped[UUID] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"), index=True, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="recommendations")
    resource: Mapped["Resource"] = relationship("Resource", back_populates="recommendations")
