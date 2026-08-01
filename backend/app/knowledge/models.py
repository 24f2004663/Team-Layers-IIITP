from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class OpportunityType(str, Enum):
    """The type format of growth or learning opportunity."""
    VIDEO = "VIDEO"
    BOOK = "BOOK"
    COURSE = "COURSE"
    PROJECT = "PROJECT"
    ARTICLE = "ARTICLE"
    PODCAST = "PODCAST"
    RESEARCH_PAPER = "RESEARCH_PAPER"
    HACKATHON = "HACKATHON"
    INTERNSHIP = "INTERNSHIP"
    MENTOR = "MENTOR"
    COMMUNITY = "COMMUNITY"
    EVENT = "EVENT"
    OPEN_SOURCE = "OPEN_SOURCE"
    CERTIFICATION = "CERTIFICATION"

class GrowthOpportunity(BaseModel):
    """Normalized payload detailing a verified learning or growth opportunity."""

    id: UUID = Field(default_factory=uuid4, description="Unique opportunity ID")
    provider: str = Field(..., description="The name of the source provider (e.g. YouTube)")
    type: OpportunityType = Field(..., description="Format classification type")
    title: str = Field(..., description="The title of the opportunity")
    description: Optional[str] = Field(None, description="Detailed text body description")
    url: str = Field(..., description="Destination link reference URL")
    difficulty: str = Field("beginner", description="Target level: beginner, intermediate, advanced")
    estimated_duration: Optional[float] = Field(None, description="Duration in hours")
    cost: float = Field(0.0, description="Cost value (0.0 represents free)")
    language: str = Field("en", description="Target ISO language code")
    tags: List[str] = Field(default_factory=list, description="Descriptive classification tags")
    skills: List[str] = Field(default_factory=list, description="Target skill names built by this resource")
    prerequisites: List[str] = Field(default_factory=list, description="Knowledge prerequisites needed")
    learning_style: str = Field("visual", description="E.g. visual, auditory, hands-on")
    quality_score: float = Field(0.0, ge=0.0, le=10.0, description="Evaluated score metric (0.0 to 10.0)")
    popularity_score: float = Field(0.0, ge=0.0, le=10.0, description="Calculated usage/popularity score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Provider specific raw context parameters")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time recorded")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time updated")
