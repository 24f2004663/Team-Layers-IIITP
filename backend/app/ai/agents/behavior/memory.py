from typing import Any, Dict, List
from uuid import UUID
from app.ai.agents.behavior.schemas import BehaviorProfile, BehaviorObservation, BehaviorPattern, BehaviorEvidence
from app.ai.agents.behavior.timeline import BehaviorSnapshot
from app.infrastructure.logging.logger import logger

class BehaviorMemoryAdapter:
    """Bridges behavior database persistence operations, evidence, and timelines."""

    async def load_profile(self, user_id: UUID) -> Dict[str, Any]:
        """Loads behavior profiles from persistent layers."""
        from app.ai.runtime.container import container
        if container.behavior_memory:
            return await container.behavior_memory.load(user_id)
        logger.warning("SQLBehaviorMemoryManager not bound. Returning mock empty memory.")
        return {}

    async def save_profile(self, user_id: UUID, profile: BehaviorProfile) -> bool:
        """Saves conformed behavior profile data."""
        from app.ai.runtime.container import container
        payload = profile.model_dump()
        payload["last_updated"] = profile.last_updated.isoformat()
        
        if container.behavior_memory:
            return await container.behavior_memory.save(user_id, payload)
        logger.warning("SQLBehaviorMemoryManager not bound. Saved to mock logs.")
        return True

    async def append_snapshot(self, state: Any, snapshot: BehaviorSnapshot) -> None:
        """Appends snapshot to persistent database timeline list."""
        logger.info("Appending snapshot to behavior timeline history.", timestamp=snapshot.timestamp.isoformat())
        
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await self.load_profile(state.user.user_id)
            timeline_list = data.get("timeline", [])
            
            snap_dict = snapshot.model_dump()
            snap_dict["timestamp"] = snap_dict["timestamp"].isoformat()
            timeline_list.append(snap_dict)
            
            await container.behavior_memory.update(state.user.user_id, {"timeline": timeline_list})

    async def save_observations(self, user_id: UUID, observations: List[BehaviorObservation]) -> bool:
        """Saves observations to memory databases."""
        from app.ai.runtime.container import container
        obs_payloads = [obs.model_dump() for obs in observations]
        for obs in obs_payloads:
            obs["id"] = str(obs["id"])
            obs["timestamp"] = obs["timestamp"].isoformat()
            
        if container.behavior_memory:
            return await container.behavior_memory.update(user_id, {"observations": obs_payloads})
        return True

    async def save_evidence(self, user_id: UUID, evidence: List[BehaviorEvidence]) -> bool:
        """Saves evidence blocks to memory databases."""
        from app.ai.runtime.container import container
        ev_payloads = [ev.model_dump() for ev in evidence]
        for ev in ev_payloads:
            ev["id"] = str(ev["id"])
            ev["observation_ids"] = [str(oid) for oid in ev["observation_ids"]]
            ev["expires_at"] = ev["expires_at"].isoformat()
            ev["created_at"] = ev["created_at"].isoformat()
            
        if container.behavior_memory:
            return await container.behavior_memory.update(user_id, {"evidence": ev_payloads})
        return True

    async def save_patterns(self, user_id: UUID, patterns: List[BehaviorPattern]) -> bool:
        """Saves compiled patterns to memory databases."""
        from app.ai.runtime.container import container
        pat_payloads = [pat.model_dump() for pat in patterns]
        for pat in pat_payloads:
            pat["trend"] = pat["trend"].value
            
        if container.behavior_memory:
            return await container.behavior_memory.update(user_id, {"patterns": pat_payloads})
        return True
