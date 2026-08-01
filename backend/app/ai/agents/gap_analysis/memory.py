from typing import Any, Dict, List
from uuid import UUID
from app.ai.agents.gap_analysis.schemas import GapAnalysisResult
from app.infrastructure.logging.logger import logger

class GapMemoryAdapter:
    """Bridges gap analysis database persistence operations."""

    async def load_gaps(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Loads historical gap analyses from persistent layers."""
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            return data.get("gap_history", [])
        return []

    async def save_gap_result(self, user_id: UUID, result: GapAnalysisResult) -> bool:
        """Saves conformed gap result to database log history."""
        from app.ai.runtime.container import container
        payload = result.model_dump(mode="json")
        payload["timestamp"] = float(time.time()) if 'time' in globals() else 0.0
        
        if container.behavior_memory:
            history = await self.load_gaps(user_id)
            history.append(payload)
            return await container.behavior_memory.update(user_id, {"gap_history": history})
        return True

import time
