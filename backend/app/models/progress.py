from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float
from app.models.base import Base

class Progress(Base):
    """User monthly/weekly quantitative metrics and progress logs model."""
    __tablename__ = "progress_records"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    growth_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    milestone_completion_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    habit_adherence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="progress_records")
