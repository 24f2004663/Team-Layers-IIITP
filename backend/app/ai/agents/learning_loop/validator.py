from app.ai.agents.learning_loop.schemas import LearningLoopAgentOutput
from app.ai.framework.errors import ValidationError

class LearningLoopValidator:
    """Performs validation checks on the compiled LearningLoopAgentOutput."""

    def validate(self, output: LearningLoopAgentOutput) -> bool:
        """Runs validation rules.
        
        Args:
            output: LearningLoopAgentOutput to check.
            
        Returns:
            bool: True if passes validation rules.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        # Ensure growth index is bounded
        if output.growth_index.composite_index < 0.0 or output.growth_index.composite_index > 1.0:
            raise ValidationError("Validation failed: growth_index composite_index must be between 0.0 and 1.0.")
            
        # Ensure calibration factor is non-zero
        if output.simulator_calibration.calibration_factor == 0.0:
            raise ValidationError("Validation failed: calibration_factor cannot be exactly zero.")
            
        return True
