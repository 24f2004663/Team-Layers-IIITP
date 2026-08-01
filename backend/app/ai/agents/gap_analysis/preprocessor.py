from typing import Any, Dict
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger

class Preprocessor:
    """Collects and normalizes Identity and Behavior profiles for Gap Analysis."""

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Loads and formats profile variables from state and DI containers.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Gathered parameters.
        """
        logger.info("GapAnalysis preprocessor active")
        
        from app.ai.runtime.container import container
        
        # Load identity profile data
        identity_data = {}
        if container.identity_memory:
            identity_data = await container.identity_memory.load(state.user.user_id)
            
        # Load behavior profile data
        behavior_data = {}
        if container.behavior_memory:
            behavior_data = await container.behavior_memory.load(state.user.user_id)
            
        return {
            "identity": identity_data,
            "behavior": behavior_data,
            "goals": [g.get("name") for g in state.goals.long_term_goals] + [state.goals.primary_focus] if state.goals else []
        }
