from typing import Any, Dict, List
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger

class Preprocessor:
    """Collects, compiles, and normalizes state and timeline events for the Identity Agent."""

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Gathers onboarding details, goals, memory, and reflection traces.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Flat dictionary of gathered values.
        """
        logger.info("Identity preprocessor active")
        
        # Gather onboarding variables from state payload or settings
        payload = state.event.payload or {}
        goals = payload.get("goals", [])
        interests = payload.get("interests", [])
        
        # If empty, fallback to primary focus from goals section
        if not goals and state.goals.primary_focus:
            goals = [state.goals.primary_focus]
            
        # Load historical profile info from memory manager if available
        from app.ai.runtime.container import container
        timeline_len = 0
        last_reason = "First initialization"
        
        if container.identity_memory:
            profile_data = await container.identity_memory.load(state.user.user_id)
            if not interests:
                interests = profile_data.get("interests", [])
            timeline = profile_data.get("timeline", [])
            timeline_len = len(timeline)
            if timeline_len > 0:
                last_reason = timeline[-1].get("reason_for_change", "First initialization")
            
        return {
            "goals": goals,
            "interests": interests,
            "previous_archetype": state.identity.archetype or "None",
            "last_change_reason": last_reason,
            "timeline_length": timeline_len
        }
