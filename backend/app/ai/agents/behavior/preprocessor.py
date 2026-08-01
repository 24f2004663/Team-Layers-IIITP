from typing import Any, Dict, List
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger

class Preprocessor:
    """Collects, compiles, and normalizes historical observations, evidence, and patterns."""

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Loads and formats the current list of observations, evidence, and patterns.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Preprocessed raw values.
        """
        logger.info("Behavior preprocessor active")
        
        observations: List[Any] = context.metadata.get("observations", [])
        evidence: List[Any] = context.metadata.get("evidence", [])
        patterns: List[Any] = context.metadata.get("patterns", [])
        
        return {
            "observations_count": len(observations),
            "evidence_count": len(evidence),
            "patterns_count": len(patterns),
            "raw_observations": [obs.model_dump() for obs in observations],
            "raw_evidence": [ev.model_dump() for ev in evidence],
            "raw_patterns": [pat.model_dump() for pat in patterns],
            "last_active": state.session.last_active.isoformat()
        }
