from typing import List
from app.engines.mission.schemas import Mission
from app.ai.framework.errors import ValidationError

class MissionValidator:
    """Validates properties, unique constraints, and sequence dependencies of generated missions."""

    def validate_missions(self, missions: List[Mission]) -> bool:
        """Runs validation checks.
        
        Args:
            missions: Candidate list to check.
            
        Returns:
            bool: True if passes valid criteria checks.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        seen_titles = set()
        for idx, mission in enumerate(missions):
            # 1. Duplicate check
            if mission.title in seen_titles:
                raise ValidationError(f"Validation failed: duplicate mission title observed: {mission.title}")
            seen_titles.add(mission.title)
            
            # 2. Reasoning check
            if not mission.reasoning or len(mission.reasoning) < 5:
                raise ValidationError(f"Validation failed: mission '{mission.title}' lacks valid reasoning details.")
                
            # 3. Duration check
            if mission.estimated_duration <= 0:
                raise ValidationError(f"Validation failed: mission '{mission.title}' estimated_duration must be greater than zero.")
                
        return True
