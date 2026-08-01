from typing import Any, Dict
from app.engines.evidence.schemas import ExecutionEvidence
from app.engines.evidence.collector import EvidenceCollector
from app.engines.evidence.validator import EvidenceValidator

class EvidenceEngine:
    """The central engine coordinating execution evidence accumulation and validation."""

    def __init__(self):
        self.collector = EvidenceCollector()
        self.validator = EvidenceValidator()

    def collect_and_validate(self, execution_data: Dict[str, Any]) -> ExecutionEvidence:
        """Accumulates evidence and runs integrity check rules.
        
        Args:
            execution_data: Raw activity payload dictionary.
            
        Returns:
            ExecutionEvidence: Collected conformed validated evidence.
        """
        evidence = self.collector.collect(execution_data)
        self.validator.validate(evidence)
        return evidence
