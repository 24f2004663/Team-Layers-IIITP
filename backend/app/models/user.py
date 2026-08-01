from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.models.base import Base

class User(Base):
    """User accounts model."""
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    identity_profile: Mapped[Optional["IdentityProfile"]] = relationship(
        "IdentityProfile", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    behavior_profile: Mapped[Optional["BehaviorProfile"]] = relationship(
        "BehaviorProfile", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    goals: Mapped[List["Goal"]] = relationship(
        "Goal", back_populates="user", cascade="all, delete-orphan"
    )
    skills: Mapped[List["Skill"]] = relationship(
        "Skill", back_populates="user", cascade="all, delete-orphan"
    )
    daily_plans: Mapped[List["DailyPlan"]] = relationship(
        "DailyPlan", back_populates="user", cascade="all, delete-orphan"
    )
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", back_populates="user", cascade="all, delete-orphan"
    )
    reflections: Mapped[List["Reflection"]] = relationship(
        "Reflection", back_populates="user", cascade="all, delete-orphan"
    )
    progress_records: Mapped[List["Progress"]] = relationship(
        "Progress", back_populates="user", cascade="all, delete-orphan"
    )
