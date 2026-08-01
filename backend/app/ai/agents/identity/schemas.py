from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class IdentityProfile(BaseModel):
    """Pydantic model containing the extracted profile properties of a user's identity."""

    identity_summary: str = Field(..., description="High-level descriptive overview of the user's archetype")
    career_goal: str = Field(..., description="The user's stated long-term career aspirations")
    mission: str = Field(..., description="The core personal mission statement")
    core_values: List[str] = Field(default_factory=list, description="Key moral or professional drivers")
    interests: List[str] = Field(default_factory=list, description="Areas of topic curiosity")
    strengths: List[str] = Field(default_factory=list, description="Core talents and capabilities")
    weaknesses: List[str] = Field(default_factory=list, description="Areas of growth or weakness")
    learning_style: str = Field("Visual", description="Preferred knowledge acquisition style")
    preferred_difficulty: str = Field("Medium", description="Tolerated challenge pace (Easy, Medium, Hard)")
    time_commitment: str = Field("5 hours/week", description="Committed time budget")
    motivation_level: str = Field("High", description="Self-reported active drive status")
    confidence_score: float = Field(0.9, description="Confidence in assessment model metrics")
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time of last profile update")

class IdentityAnalysis(BaseModel):
    """Analytic reasoning outputs backing identity mapping actions."""

    observations: List[str] = Field(default_factory=list, description="Observed patterns or details")
    reasoning: str = Field(..., description="Chain of thought reasoning justifying profile archetypes")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Overall confidence score")
    missing_information: List[str] = Field(default_factory=list, description="Questions or details missing from onboarding")
