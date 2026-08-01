from datetime import datetime, timezone
from typing import Any, Dict
from app.ai.agents.behavior.schemas import BehaviorObservation
from app.ai.graph.events import SystemEvent

class ObservationExtractor:
    """Extracts conformed BehaviorObservations from raw state trigger events."""

    def extract_observation(self, event_type: SystemEvent, payload: Dict[str, Any]) -> BehaviorObservation:
        """Converts raw payloads and trigger keys into a conformed BehaviorObservation structure.
        
        Args:
            event_type: The SystemEvent trigger type.
            payload: Payload properties.
            
        Returns:
            BehaviorObservation: Populated observation model.
        """
        now = datetime.now(timezone.utc)
        
        duration = payload.get("duration_minutes", 0)
        context = payload.get("context", {})
        
        # Determine source
        source = payload.get("source", "SystemTrigger")
        
        # Normalize event description
        if event_type == SystemEvent.TASK_COMPLETED:
            description = f"Completed task: {payload.get('task_name', 'Unnamed task')}"
            if duration > 0:
                description += f" (Duration: {duration} mins)"
        elif event_type == SystemEvent.TASK_SKIPPED:
            description = f"Skipped task: {payload.get('task_name', 'Unnamed task')} - possible procrastination."
            context["procrastination_signal"] = True
        elif event_type == SystemEvent.RESOURCE_COMPLETED:
            description = f"Completed resource: {payload.get('resource_title', 'Unnamed resource')}"
        elif event_type == SystemEvent.DAY_ENDED:
            description = "Completed daily schedule checks and day summary compiling."
        elif event_type == SystemEvent.WEEK_ENDED:
            description = "Completed weekly reflections review and progress updates."
        elif event_type == SystemEvent.USER_LOGIN:
            description = "Recorded user login session status."
        else:
            description = f"Trigger event observed: {event_type.value}"
            
        return BehaviorObservation(
            timestamp=now,
            event_type=event_type.value,
            source=source,
            description=description,
            duration=duration,
            context=context,
            confidence=1.0
        )
