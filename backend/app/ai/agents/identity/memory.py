from typing import Any, Dict, List
from uuid import UUID
from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.domain.identity_timeline import IdentitySnapshot
from app.infrastructure.logging.logger import logger

class IdentityMemoryAdapter:
    """Bridges database identity memory operations and manages timeline snapshot appends."""

    async def load_profile(self, user_id: UUID) -> Dict[str, Any]:
        """Loads raw profile properties from database layers.
        
        Args:
            user_id: User UUID.
            
        Returns:
            Dict[str, Any]: Loaded values.
        """
        from app.ai.runtime.container import container
        if container.identity_memory:
            return await container.identity_memory.load(user_id)
        logger.warning("SQLIdentityMemoryManager not bound. Returning mock memory payload.")
        return {}

    async def save_profile(self, user_id: UUID, profile: IdentityProfile) -> bool:
        """Saves conformed profile properties.
        
        Args:
            user_id: User UUID.
            profile: IdentityProfile to persist.
            
        Returns:
            bool: True if save operation succeeded.
        """
        payload = profile.model_dump()
        # Convert datetime to string serialization compat if required
        payload["last_updated"] = profile.last_updated.isoformat()
        
        from app.ai.runtime.container import container
        if container.identity_memory:
            return await container.identity_memory.save(user_id, payload)
        logger.warning("SQLIdentityMemoryManager not bound. Saved to mock logs.")
        return True

    async def append_snapshot(self, state: Any, snapshot: IdentitySnapshot) -> None:
        """Appends the identity snapshot to the active timeline list in persistent database.
        
        Args:
            state: Active LifeGPSState.
            snapshot: New snapshot to record.
        """
        logger.info("Appending snapshot to identity timeline history.", timestamp=snapshot.timestamp.isoformat())
        
        from app.ai.runtime.container import container
        if container.identity_memory:
            data = await self.load_profile(state.user.user_id)
            timeline_list = data.get("timeline", [])
            
            snap_dict = snapshot.model_dump()
            snap_dict["timestamp"] = snap_dict["timestamp"].isoformat()
            timeline_list.append(snap_dict)
            
            await container.identity_memory.update(state.user.user_id, {"timeline": timeline_list})
