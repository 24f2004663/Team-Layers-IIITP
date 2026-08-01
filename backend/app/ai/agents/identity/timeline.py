from datetime import datetime, timezone
from typing import List
from app.ai.domain.identity_timeline import IdentitySnapshot
from app.ai.agents.identity.schemas import IdentityProfile

class TimelineHelper:
    """Helper class parsing agent output profiles into timeline IdentitySnapshot domain models."""

    def create_snapshot(
        self, 
        profile: IdentityProfile, 
        skills: List[str], 
        goals: List[str], 
        reason: str
    ) -> IdentitySnapshot:
        """Constructs a new IdentitySnapshot to append to the user history.
        
        Args:
            profile: Active generated IdentityProfile.
            skills: User active skills.
            goals: Long term goals list.
            reason: Change context justification.
            
        Returns:
            IdentitySnapshot: Formatted snapshot model.
        """
        return IdentitySnapshot(
            timestamp=datetime.now(timezone.utc),
            identity_summary=profile.identity_summary,
            career_goal=profile.career_goal,
            interests=profile.interests,
            skills=skills,
            goals=goals,
            reason_for_change=reason,
            confidence=profile.confidence_score
        )
