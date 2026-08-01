from typing import Any, Dict
from app.engines.evidence.schemas import ExecutionEvidence

class EvidenceCollector:
    """Collects evidence metrics from logged user interactions and calendar schedules."""

    def collect(self, execution_data: Dict[str, Any]) -> ExecutionEvidence:
        """Assembles metrics into the conformed ExecutionEvidence model.
        
        Args:
            execution_data: Raw activity payload dictionary.
            
        Returns:
            ExecutionEvidence: Collected conformed evidence.
        """
        return ExecutionEvidence(
            completed_missions_count=execution_data.get("completed_missions", 1),
            completed_execution_units=execution_data.get("completed_units", 3),
            session_duration_minutes=execution_data.get("session_duration", 90),
            interruptions_count=execution_data.get("interruptions", 1),
            mood_value=execution_data.get("mood", "Focused"),
            energy_level=execution_data.get("energy", "High"),
            error_logs_count=execution_data.get("errors", 0),
            user_feedback_score=execution_data.get("feedback_score", 0.90)
        )
