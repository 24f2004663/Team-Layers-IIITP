import pytest
from app.ai.graph.events import SystemEvent
from app.ai.graph.router import WorkflowRouter

def test_system_event_resolutions():
    """Verify that every defined SystemEvent resolves cleanly to a workflow via WorkflowRouter."""
    router = WorkflowRouter()
    
    # List of all system events that should trigger workflows
    events_to_test = [
        SystemEvent.USER_ONBOARDED,
        SystemEvent.USER_LOGIN,
        SystemEvent.GOAL_UPDATED,
        SystemEvent.TASK_COMPLETED,
        SystemEvent.TASK_SKIPPED,
        SystemEvent.RESOURCE_STARTED,
        SystemEvent.RESOURCE_COMPLETED,
        SystemEvent.RESOURCE_ABANDONED,
        SystemEvent.DAY_ENDED,
        SystemEvent.WEEK_ENDED,
        SystemEvent.SESSION_STARTED,
        SystemEvent.SESSION_ENDED,
        SystemEvent.REFLECTION_SUBMITTED,
        SystemEvent.MIDNIGHT_SYNC
    ]
    
    for event in events_to_test:
        workflow = router.resolve(event)
        assert workflow is not None
        assert workflow.name is not None
        assert len(workflow.stages) > 0
