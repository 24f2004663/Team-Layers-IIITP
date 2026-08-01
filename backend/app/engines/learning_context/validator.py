from app.engines.learning_context.schemas import LearningContext
from app.ai.framework.errors import ValidationError

class LearningContextValidator:
    """Validates structural fields and focus variables of the compiled LearningContext."""

    def validate(self, context: LearningContext) -> bool:
        """Validates bounds.
        
        Args:
            context: LearningContext to check.
            
        Returns:
            bool: True if passes checks.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        if context.available_time <= 0:
            raise ValidationError("Validation failed: available_time must be greater than zero.")
            
        if context.attention_span <= 0:
            raise ValidationError("Validation failed: attention_span must be greater than zero.")
            
        return True
