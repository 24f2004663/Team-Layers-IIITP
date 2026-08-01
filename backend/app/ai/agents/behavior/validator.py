from app.ai.agents.behavior.schemas import BehaviorProfile
from app.ai.framework.errors import ValidationError
from app.ai.validator.confidence_validator import ConfidenceValidator

class BehaviorValidator:
    """Performs structural and logic boundary validations on the generated BehaviorProfile."""

    def __init__(self, min_confidence: float = 0.70):
        self.confidence_validator = ConfidenceValidator(min_confidence=min_confidence)

    def validate(self, profile: BehaviorProfile) -> bool:
        """Runs validation rules.
        
        Args:
            profile: BehaviorProfile to check.
            
        Returns:
            bool: True if passes validation rules.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        # 1. Attention span check
        if profile.attention_span_minutes <= 0:
            raise ValidationError("Validation failed: attention_span_minutes must be greater than zero.")
            
        # 2. Productive hours check
        for hour in profile.productive_hours:
            if hour < 0 or hour > 23:
                raise ValidationError(f"Validation failed: hour {hour} in productive_hours is out of bounds (0-23).")
                
        # 3. Confidence score check
        if not self.confidence_validator.validate_confidence(profile.confidence_score):
            raise ValidationError(f"Validation failed: confidence_score {profile.confidence_score} is below threshold.")
            
        return True
