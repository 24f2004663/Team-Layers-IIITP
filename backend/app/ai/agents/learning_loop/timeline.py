from datetime import datetime, timezone
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class GrowthTimelineSnapshot(BaseModel):
    """Domain model capturing a user's personal growth index scores at a specific point in time."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Snapshot timestamp")
    composite_growth_index: float = Field(..., description="Personal growth index score")
    weekly_trajectory_change: float = Field(..., description="Trajectory match percentage delta")
    primary_reflection_summary: str = Field(..., description="Short summary of daily reflection findings")

class LearningLoopTimelineHelper:
    """Helper formatting snapshots and transitions from learning loop performance trends."""

    def create_snapshot(
        self,
        growth_index: float,
        trajectory_change: float,
        reflection_summary: str
    ) -> GrowthTimelineSnapshot:
        """Constructs a GrowthTimelineSnapshot.
        
        Args:
            growth_index: Personal growth index rating.
            trajectory_change: Weekly trajectory difference rate.
            reflection_summary: Reflection text.
            
        Returns:
            GrowthTimelineSnapshot: Timeline snapshot model.
        """
        return GrowthTimelineSnapshot(
            timestamp=datetime.now(timezone.utc),
            composite_growth_index=growth_index,
            weekly_trajectory_change=trajectory_change,
            primary_reflection_summary=reflection_summary
        )
