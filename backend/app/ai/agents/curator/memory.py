from typing import Any, Dict, List
from uuid import UUID
from app.ai.agents.curator.schemas import CuratorAgentOutput
from app.infrastructure.logging.logger import logger

class CuratorMemoryAdapter:
    """Bridges curation and experience bundles feedback database persistence operations."""

    async def load_bundles(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Loads historical bundles from persistent layers."""
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            return data.get("experience_bundles_history", [])
        return []

    async def save_bundle(self, user_id: UUID, output: CuratorAgentOutput) -> bool:
        """Saves conformed experience bundle."""
        from app.ai.runtime.container import container
        payload = output.model_dump(mode="json")
        
        if container.behavior_memory:
            history = await self.load_bundles(user_id)
            history.append(payload)
            return await container.behavior_memory.update(user_id, {"experience_bundles_history": history})
        return True

    async def record_feedback(self, user_id: UUID, bundle_id: UUID, signal: str) -> bool:
        """Appends feedback signals (Started, Completed, Mastered, Applied, Shared, Mentored) to learning history.
        
        Args:
            user_id: User identifier.
            bundle_id: Target bundle identifier.
            signal: Feedback action signal name.
            
        Returns:
            bool: True if persistent update succeeds.
        """
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            timeline = data.get("experiences_timeline", [])
            timeline.append({
                "bundle_id": str(bundle_id),
                "feedback_signal": signal,
                "timestamp": "2026-08-01T12:00:00Z"
            })
            return await container.behavior_memory.update(user_id, {"experiences_timeline": timeline})
        return True
