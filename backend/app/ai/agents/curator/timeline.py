from datetime import datetime, timezone
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class ExperienceTimelineSnapshot(BaseModel):
    """Domain model capturing a user's mastered learning experiences at a specific point in time."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Snapshot timestamp")
    primary_video: str = Field(..., description="Main video URL")
    expected_gains_summary: str = Field(..., description="Skill gains overview")
    outcome_explanation: str = Field(..., description="Explainability outcomes mapping")

class CuratorTimelineHelper:
    """Helper formatting snapshots and transitions from learning history trends."""

    def create_snapshot(
        self,
        video: str,
        gains: List[Any],
        outcome: str
    ) -> ExperienceTimelineSnapshot:
        """Constructs an ExperienceTimelineSnapshot.
        
        Args:
            video: Primary video link.
            gains: Expected skill gains.
            outcome: Outcome text.
            
        Returns:
            ExperienceTimelineSnapshot: Snapshot instance.
        """
        gains_text = ", ".join([f"{g.skill_name}: +{g.gain_percentage * 100}%" for g in gains]) if hasattr(gains[0], "skill_name") else str(gains)
        return ExperienceTimelineSnapshot(
            timestamp=datetime.now(timezone.utc),
            primary_video=video,
            expected_gains_summary=gains_text,
            outcome_explanation=outcome
        )
