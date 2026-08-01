from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.framework.errors import ValidationError
from app.ai.validator.confidence_validator import ConfidenceValidator

class IdentityValidator:
    """Performs structural and logic sanity boundary checks on the generated IdentityProfile."""

    def __init__(self, min_confidence: float = 0.70):
        self.confidence_validator = ConfidenceValidator(min_confidence=min_confidence)

    def validate(self, profile: IdentityProfile) -> bool:
        """Runs required field and confidence score checks on the profile.
        
        Args:
            profile: Candidate IdentityProfile.
            
        Returns:
            bool: True if passes validation rules.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        # 1. Career goal check
        if not profile.career_goal or profile.career_goal.strip() == "":
            raise ValidationError("Validation failed: career_goal must be a non-empty string.")
            
        # 2. Identity summary check
        if not profile.identity_summary or profile.identity_summary.strip() == "":
            raise ValidationError("Validation failed: identity_summary must be a non-empty string.")
            
        # 3. Interests check
        if not profile.interests or len(profile.interests) == 0:
            raise ValidationError("Validation failed: interests list cannot be empty.")
            
        for interest in profile.interests:
            if not interest or interest.strip() == "":
                raise ValidationError("Validation failed: interest value cannot be empty.")
                
        # 4. Confidence check
        if not self.confidence_validator.validate_confidence(profile.confidence_score):
            raise ValidationError(f"Validation failed: confidence_score {profile.confidence_score} is below threshold.")
            
        return True
