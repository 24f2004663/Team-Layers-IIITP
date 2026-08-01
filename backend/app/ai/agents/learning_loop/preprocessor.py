from typing import Any, Dict
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger
from app.engines.evidence.engine import EvidenceEngine
from app.engines.outcome.engine import OutcomeEngine

class Preprocessor:
    """Orchestrates evidence collection and outcome parsing pipelines."""

    def __init__(self):
        self.evidence_engine = EvidenceEngine()
        self.outcome_engine = OutcomeEngine()

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Runs engines on active payload metrics to resolve collected outputs.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Preprocessed parameters.
        """
        logger.info("Learning Loop preprocessor active")
        
        # Load logged metrics from context metadata
        logged_data = context.metadata.get("execution_data", {
            "completed_missions": 1,
            "completed_units": 2,
            "session_duration": 60,
            "interruptions": 0,
            "mood": "Focused",
            "energy": "High",
            "errors": 0,
            "feedback_score": 0.95
        })
        
        # Accumulate conformed evidence
        evidence = self.evidence_engine.collect_and_validate(logged_data)
        context.metadata["execution_evidence"] = evidence
        
        # Run outcome analyzer
        outcome = self.outcome_engine.analyze(evidence)
        context.metadata["outcome_analysis"] = outcome
        
        # Load profiles
        from app.ai.runtime.container import container
        identity_data = {}
        behavior_data = {}
        if container.identity_memory:
            identity_data = await container.identity_memory.load(state.user.user_id)
        if container.behavior_memory:
            behavior_data = await container.behavior_memory.load(state.user.user_id)
            
        return {
            "evidence": evidence.model_dump(),
            "outcome": outcome.model_dump(),
            "identity": identity_data,
            "behavior": behavior_data
        }
