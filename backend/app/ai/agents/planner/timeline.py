from datetime import datetime, timezone
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class PlannerTimelineSnapshot(BaseModel):
    """Domain model capturing a user's active daily schedule allocations at a specific point in time."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Snapshot timestamp")
    date: str = Field(..., description="Target date string YYYY-MM-DD")
    total_focused_minutes: int = Field(..., description="Focus allocation duration minutes")
    agenda_titles: List[str] = Field(default_factory=list, description="List of scheduled task titles")
    reason_for_change: str = Field(..., description="Context for schedule modifications")

class PlannerTimelineHelper:
    """Helper formatting snapshots and transitions from calendar plans history trends."""

    def create_snapshot(
        self,
        date: str,
        total_focused_minutes: int,
        agenda: List[Any],
        reason: str
    ) -> PlannerTimelineSnapshot:
        """Constructs a PlannerTimelineSnapshot.
        
        Args:
            date: Target date.
            total_focused_minutes: Focus duration.
            agenda: List of items.
            reason: Justification statement.
            
        Returns:
            PlannerTimelineSnapshot: Populated snapshot model.
        """
        titles = [item.title for item in agenda]
        return PlannerTimelineSnapshot(
            timestamp=datetime.now(timezone.utc),
            date=date,
            total_focused_minutes=total_focused_minutes,
            agenda_titles=titles,
            reason_for_change=reason
        )
