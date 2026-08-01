from typing import Any, Dict, List
from uuid import UUID
from app.ai.agents.learning_loop.schemas import LearningLoopAgentOutput
from app.infrastructure.logging.logger import logger

class LearningLoopMemoryAdapter:
    """Bridges learning loop reflections, calibration logs, and delta trends persistence operations."""

    async def save_reflection(self, user_id: UUID, output: LearningLoopAgentOutput) -> bool:
        """Saves conformed reflections, calibrations, and indices history log dicts."""
        from app.ai.runtime.container import container
        payload = output.model_dump(mode="json")
        
        if container.behavior_memory:
            # 1. Update reflections history
            data = await container.behavior_memory.load(user_id)
            ref_list = data.get("reflections_history", [])
            ref_list.append(payload.get("reflection", {}))
            
            # 2. Update growth deltas history
            growth_list = data.get("growth_history", [])
            growth_list.append(payload.get("growth_delta", {}))
            
            # 3. Update simulator calibration logs
            cal_list = data.get("calibration_history", [])
            cal_list.append(payload.get("simulator_calibration", {}))
            
            # 4. Save updates
            return await container.behavior_memory.update(user_id, {
                "reflections_history": ref_list,
                "growth_history": growth_list,
                "calibration_history": cal_list
            })
        return True
