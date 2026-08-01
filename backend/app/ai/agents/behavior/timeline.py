from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel, Field
from app.ai.agents.behavior.schemas import BehaviorProfile, BehaviorPattern

class BehaviorSnapshot(BaseModel):
    """Domain model capturing a user's behavioral state and pattern transitions at a specific point in time."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Snapshot timestamp")
    summary: str = Field(..., description="High-level summary of behavioral patterns")
    patterns: List[str] = Field(default_factory=list, description="Active pattern names")
    productive_hours: List[int] = Field(default_factory=list, description="Hours of peak performance")
    attention_span: int = Field(..., description="Average focus span in minutes")
    motivation: str = Field(..., description="Assessed motivation level")
    reason_for_change: str = Field(..., description="Context for snapshot updates")
    confidence: float = Field(..., description="Confidence rating")

class BehaviorTimelineHelper:
    """Helper formatting snapshots and transitions from profile history trends."""

    def create_snapshot(
        self, 
        profile: BehaviorProfile, 
        patterns: List[BehaviorPattern], 
        reason: str
    ) -> BehaviorSnapshot:
        """Constructs a BehaviorSnapshot.
        
        Args:
            profile: Source BehaviorProfile.
            patterns: Identified BehaviorPattern list.
            reason: Change update reasoning context.
            
        Returns:
            BehaviorSnapshot: Populated snapshot model.
        """
        pattern_names = [f"{pat.pattern_name} ({pat.trend.value})" for pat in patterns]
        summary_text = f"User focus style resolved as {profile.focus_style} with average span of {profile.attention_span_minutes} minutes."
        
        return BehaviorSnapshot(
            timestamp=datetime.now(timezone.utc),
            summary=summary_text,
            patterns=pattern_names,
            productive_hours=profile.productive_hours,
            attention_span=profile.attention_span_minutes,
            motivation=profile.motivation_level,
            reason_for_change=reason,
            confidence=profile.confidence_score
        )
