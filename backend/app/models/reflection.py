from typing import Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, JSON
from app.models.base import Base

class Reflection(Base):
    """User daily/weekly reflection reviews and cognitive insights logs model."""
    __tablename__ = "reflections"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    prompts: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    responses: Mapped[Dict[str, str]] = mapped_column(JSON, default=dict, nullable=False)
    synthesized_insight: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reflections")
