from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from app.models.base import Base

class Resource(Base):
    """Learning materials, videos, exercises, and general growth resources model."""
    __tablename__ = "resources"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", back_populates="resource", cascade="all, delete-orphan"
    )
