from typing import Any, Dict, List
from uuid import UUID
from app.ai.agents.planner.schemas import PlannerAgentOutput
from app.infrastructure.logging.logger import logger

class PlannerMemoryAdapter:
    """Bridges planner database persistence operations."""

    async def load_plans(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Loads historical plans from persistent layers."""
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            return data.get("plans_history", [])
        return []

    async def save_plan(self, user_id: UUID, output: PlannerAgentOutput) -> bool:
        """Saves conformed daily/weekly/monthly plans list."""
        from app.ai.runtime.container import container
        payload = output.model_dump(mode="json")
        
        if container.behavior_memory:
            history = await self.load_plans(user_id)
            history.append(payload)
            return await container.behavior_memory.update(user_id, {"plans_history": history})
        return True
