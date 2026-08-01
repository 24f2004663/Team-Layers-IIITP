from typing import Any, Dict
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext

class ContextBuilder:
    """Compiles state, context, and custom variables into a single flat context payload dictionary."""

    def build_context(
        self, 
        state: LifeGPSState, 
        context: ExecutionContext, 
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merges all state properties and additional variables.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            variables: Custom dictionary variables.
            
        Returns:
            Dict[str, Any]: Merged payload context.
        """
        # Expose common state properties to prompt template matching
        return {
            "user_id": str(state.user.user_id),
            "timezone": state.user.timezone,
            "event": context.event.value,
            "stage": context.current_stage.value,
            "completed_agents": ", ".join(context.completed_agents),
            "archetype": state.identity.archetype,
            "core_values": ", ".join(state.identity.core_values),
            "strengths": ", ".join(state.identity.strengths),
            "weaknesses": ", ".join(state.identity.weaknesses),
            **variables
        }
