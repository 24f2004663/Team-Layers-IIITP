from app.engines.evidence.schemas import ExecutionEvidence
from app.engines.outcome.schemas import OutcomeAnalysis
from app.engines.outcome.metrics import OutcomeMetricsCalculator

class OutcomeEngine:
    """The central engine coordinating performance outcome analytics calculation."""

    def __init__(self):
        self.calculator = OutcomeMetricsCalculator()

    def analyze(self, evidence: ExecutionEvidence) -> OutcomeAnalysis:
        """Runs the calculation pipeline on accumulated evidence metrics.
        
        Args:
            evidence: Collected ExecutionEvidence.
            
        Returns:
            OutcomeAnalysis: Calculated conformed outcome analysis parameters.
        """
        return self.calculator.calculate_analysis(evidence)
