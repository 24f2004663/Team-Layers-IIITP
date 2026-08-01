from app.ai.agents.curator.schemas import CuratorAgentOutput
from app.ai.framework.errors import ValidationError

class CuratorValidator:
    """Performs validation checks on the curated ExperienceBundle."""

    def validate(self, output: CuratorAgentOutput) -> bool:
        """Runs validation rules.
        
        Args:
            output: CuratorAgentOutput to check.
            
        Returns:
            bool: True if passes validation rules.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        # Ensure completion time is valid
        if output.bundle.estimated_completion_time_minutes <= 0:
            raise ValidationError("Validation failed: estimated_completion_time_minutes must be greater than zero.")
            
        # Verify confidence range
        if output.bundle.explanation.confidence < 0.0 or output.bundle.explanation.confidence > 1.0:
            raise ValidationError("Validation failed: confidence must be between 0.0 and 1.0.")
            
        return True
