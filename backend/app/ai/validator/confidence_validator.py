from app.infrastructure.logging.logger import logger

class ConfidenceValidator:
    """Verifies that agent outputs satisfy minimum confidence requirements."""

    def __init__(self, min_confidence: float = 0.7):
        """Initializes the validator.
        
        Args:
            min_confidence: Minimum float score required.
        """
        self.min_confidence = min_confidence

    def validate_confidence(self, score: float) -> bool:
        """Checks if confidence score is above minimum threshold.
        
        Args:
            score: Confidence value score (0.0 to 1.0).
            
        Returns:
            bool: True if passes.
        """
        if score < self.min_confidence:
            logger.warning(f"Confidence score {score} falls below minimum threshold {self.min_confidence}.")
            return False
        return True
