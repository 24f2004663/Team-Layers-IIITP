from app.engines.evidence.schemas import ExecutionEvidence
from app.ai.framework.errors import ValidationError

class EvidenceValidator:
    """Validates structural properties and thresholds of accumulated ExecutionEvidence."""

    def validate(self, evidence: ExecutionEvidence) -> bool:
        """Validates bounds.
        
        Args:
            evidence: ExecutionEvidence to check.
            
        Returns:
            bool: True if passes checks.
            
        Raises:
            ValidationError: If boundaries are failed.
        """
        if evidence.session_duration_minutes < 0:
            raise ValidationError("Validation failed: session_duration_minutes cannot be negative.")
            
        if evidence.user_feedback_score < 0.0 or evidence.user_feedback_score > 1.0:
            raise ValidationError("Validation failed: user_feedback_score must be between 0.0 and 1.0.")
            
        return True
