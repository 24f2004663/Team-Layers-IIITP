from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

class PatternStability(str, Enum):
    """Stability levels tracking how consistent a user pattern behaves over time."""
    NEW = "NEW"
    EMERGING = "EMERGING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"
    EXPIRED = "EXPIRED"

class BehaviorProfile(BaseModel):
    """The normalized profile reflecting the user's natural work behaviors."""

    learning_style: str = Field("Visual", description="Derived learning acquisition style")
    focus_style: str = Field("Spurt", description="Derived concentration pattern (e.g. Pomodoro, Deep Work, Spurt)")
    attention_span_minutes: int = Field(30, description="Evaluated average continuous focus span")
    productive_hours: List[int] = Field(default_factory=list, description="Hours of peak performance (0-23)")
    preferred_session_length: int = Field(45, description="Ideal duration of a single learning session")
    procrastination_level: str = Field("Low", description="Evaluated procrastination score (Low, Medium, High)")
    consistency_score: float = Field(0.8, description="Streak adherence consistency score (0.0 to 1.0)")
    adaptability_score: float = Field(0.7, description="Pace/schedule change adaptation score")
    motivation_level: str = Field("Medium", description="Evaluated drive status")
    energy_pattern: str = Field("Morning Peak", description="Hourly energy levels pattern")
    stress_pattern: str = Field("Stable", description="Daily stress indicator")
    confidence_score: float = Field(0.9, description="Evaluation confidence metric")
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Last update time")

class BehaviorObservation(BaseModel):
    """A normalized user action event mapped for behavioral analytics."""

    id: UUID = Field(default_factory=uuid4, description="Unique observation ID")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time observation occurred")
    event_type: str = Field(..., description="Action trigger event type")
    source: str = Field(..., description="Trigger source component name")
    description: str = Field(..., description="Detailed description of the behavioral observation")
    duration: int = Field(0, description="Event duration in minutes")
    context: Dict[str, Any] = Field(default_factory=dict, description="Metadata parameters captured")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom parameters")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Base confidence weight of observation")

class BehaviorEvidence(BaseModel):
    """Synthesized evidence block matching observations to a behavioral hypothesis."""

    id: UUID = Field(default_factory=uuid4, description="Unique evidence ID")
    observation_ids: List[UUID] = Field(default_factory=list, description="Associated observation IDs")
    hypothesis: str = Field(..., description="The behavioral hypothesis (e.g. Night Learner)")
    support_score: float = Field(..., description="Evaluated support strength ratio")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this evidence hypothesis")
    expires_at: datetime = Field(..., description="Confidence expiration timestamp")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Created timestamp")

class BehaviorPattern(BaseModel):
    """An analyzed behavioral pattern synthesized from multiple evidences."""

    pattern_name: str = Field(..., description="Descriptive name of behavior pattern")
    supporting_observations: List[str] = Field(default_factory=list, description="Descriptions of supporting observations")
    frequency: int = Field(1, description="Observation matches count")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Aggregated confidence metric")
    trend: PatternStability = Field(PatternStability.NEW, description="Pattern stability classification status")

class GrowthInsight(BaseModel):
    """Contextual insight identifying focus gaps and opportunities for personal growth."""

    title: str = Field(..., description="Summary title of the insight")
    description: str = Field(..., description="Clear explanation of the behavioral insight")
    evidence: str = Field(..., description="Summary of evidence points backing this insight")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence of the insight")
    recommended_focus: str = Field(..., description="Recommended focus pivot area")

class BehaviorAgentOutput(BaseModel):
    """The rich conformed output model returned by the Behavior Agent."""

    profile: BehaviorProfile = Field(..., description="The updated behavior profile")
    observations: List[BehaviorObservation] = Field(default_factory=list, description="Collected observations")
    evidence: List[BehaviorEvidence] = Field(default_factory=list, description="Constructed evidences")
    patterns: List[BehaviorPattern] = Field(default_factory=list, description="Synthesized patterns")
    alignment: Any = Field(None, description="Current identity alignment result")
    growth_insights: List[GrowthInsight] = Field(default_factory=list, description="Identified growth opportunities")
    timeline_snapshot: Any = Field(None, description="Appended snapshot details")
