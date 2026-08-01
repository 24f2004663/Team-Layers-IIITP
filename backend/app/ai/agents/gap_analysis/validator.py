from app.ai.agents.gap_analysis.schemas import GapAnalysisResult
from app.ai.framework.errors import ValidationError

class GapValidator:
    """Performs structural and logic boundary validations on the generated GapAnalysisResult."""

    def validate(self, result: GapAnalysisResult) -> bool:
        """Runs validation rules.
        
        Args:
            result: GapAnalysisResult to check.
            
        Returns:
            bool: True if passes validation rules.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        if result.overall_gap_score < 0.0 or result.overall_gap_score > 1.0:
            raise ValidationError("Validation failed: overall_gap_score must be between 0.0 and 1.0.")
            
        if result.confidence < 0.70:
            raise ValidationError(f"Validation failed: confidence {result.confidence} is below threshold.")
            
        return True
