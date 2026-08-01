from typing import Any, Dict, List
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger

class Preprocessor:
    """Gathers and normalizes the prioritized mission list and behavioral work style parameters."""

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Loads required values from execution context metadata and persistent layers.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Preprocessed parameters.
        """
        logger.info("Planner preprocessor active")
        
        # Load prioritized mission list from execution context metadata
        missions: List[Any] = context.metadata.get("missions", [])
        
        # Load behavior profile to retrieve attention span and focus window requirements
        from app.ai.runtime.container import container
        behavior_data = {}
        if container.behavior_memory:
            behavior_data = await container.behavior_memory.load(state.user.user_id)
            
        return {
            "missions": [m.model_dump() for m in missions],
            "behavior_profile": behavior_data,
            "available_hours_per_day": 3.0,
            "today_date": state.session.last_active.date().isoformat()
        }
