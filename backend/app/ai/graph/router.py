from typing import Dict
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowDefinition, WorkflowStage

class WorkflowRouter:
    """Router resolving SystemEvents into stage-based WorkflowDefinitions."""

    def __init__(self):
        self._routes: Dict[SystemEvent, WorkflowDefinition] = {
            SystemEvent.USER_LOGIN: WorkflowDefinition(
                name="USER_LOGIN_FLOW",
                description="Adapts plans and processes habit patterns upon user login.",
                trigger_event=SystemEvent.USER_LOGIN,
                stages=[
                    WorkflowStage.PRE_PROCESS,
                    WorkflowStage.ANALYSIS,
                    WorkflowStage.PLANNING,
                    WorkflowStage.CURATION,
                    WorkflowStage.POST_PROCESS
                ]
            ),
            SystemEvent.USER_ONBOARDED: WorkflowDefinition(
                name="USER_ONBOARDING_FLOW",
                description="Initiates onboarding analysis and seed plans.",
                trigger_event=SystemEvent.USER_ONBOARDED,
                stages=[
                    WorkflowStage.ANALYSIS,
                    WorkflowStage.PLANNING,
                    WorkflowStage.CURATION
                ]
            ),
            SystemEvent.GOAL_UPDATED: WorkflowDefinition(
                name="GOAL_UPDATED_FLOW",
                description="Updates goals, milestone roadmaps, and content curations.",
                trigger_event=SystemEvent.GOAL_UPDATED,
                stages=[
                    WorkflowStage.PLANNING,
                    WorkflowStage.KNOWLEDGE,
                    WorkflowStage.CURATION
                ]
            ),
            SystemEvent.TASK_COMPLETED: WorkflowDefinition(
                name="TASK_COMPLETED_FLOW",
                description="Updates milestone completion and reflection states on task checkoff.",
                trigger_event=SystemEvent.TASK_COMPLETED,
                stages=[
                    WorkflowStage.POST_PROCESS,
                    WorkflowStage.MEMORY_UPDATE,
                    WorkflowStage.PLANNING
                ]
            ),
            SystemEvent.REFLECTION_SUBMITTED: WorkflowDefinition(
                name="REFLECTION_SUBMITTED_FLOW",
                description="Analyzes reflection logs to adjust streak scores and next plan.",
                trigger_event=SystemEvent.REFLECTION_SUBMITTED,
                stages=[
                    WorkflowStage.POST_PROCESS,
                    WorkflowStage.ANALYSIS,
                    WorkflowStage.PLANNING,
                    WorkflowStage.CURATION
                ]
            ),
            SystemEvent.DAY_STARTED: WorkflowDefinition(
                name="DAY_STARTED_FLOW",
                description="Plans priority slots and checks daily target parameters.",
                trigger_event=SystemEvent.DAY_STARTED,
                stages=[
                    WorkflowStage.PLANNING,
                    WorkflowStage.CURATION
                ]
            ),
            SystemEvent.DAY_ENDED: WorkflowDefinition(
                name="DAY_ENDED_FLOW",
                description="Compiles statistics and updates active progress memory.",
                trigger_event=SystemEvent.DAY_ENDED,
                stages=[
                    WorkflowStage.POST_PROCESS,
                    WorkflowStage.MEMORY_UPDATE
                ]
            ),
            SystemEvent.PROFILE_UPDATED: WorkflowDefinition(
                name="PROFILE_UPDATED_FLOW",
                description="Updates archetype character map and alignment configurations.",
                trigger_event=SystemEvent.PROFILE_UPDATED,
                stages=[
                    WorkflowStage.ANALYSIS,
                    WorkflowStage.PLANNING
                ]
            ),
            SystemEvent.SYSTEM_SYNC: WorkflowDefinition(
                name="SYSTEM_SYNC_FLOW",
                description="Triggers transient session caches synchronization.",
                trigger_event=SystemEvent.SYSTEM_SYNC,
                stages=[
                    WorkflowStage.POST_PROCESS
                ]
            ),
            SystemEvent.TASK_SKIPPED: WorkflowDefinition(
                name="TASK_SKIPPED_FLOW",
                description="Triggered when task is skipped.",
                trigger_event=SystemEvent.TASK_SKIPPED,
                stages=[WorkflowStage.PLANNING]
            ),
            SystemEvent.RESOURCE_STARTED: WorkflowDefinition(
                name="RESOURCE_STARTED_FLOW",
                description="Triggered when learning resource starts.",
                trigger_event=SystemEvent.RESOURCE_STARTED,
                stages=[WorkflowStage.CURATION]
            ),
            SystemEvent.RESOURCE_ABANDONED: WorkflowDefinition(
                name="RESOURCE_ABANDONED_FLOW",
                description="Triggered when learning resource is abandoned.",
                trigger_event=SystemEvent.RESOURCE_ABANDONED,
                stages=[WorkflowStage.ANALYSIS]
            ),
            SystemEvent.SESSION_STARTED: WorkflowDefinition(
                name="SESSION_STARTED_FLOW",
                description="Triggered when session starts.",
                trigger_event=SystemEvent.SESSION_STARTED,
                stages=[WorkflowStage.PRE_PROCESS]
            ),
            SystemEvent.SESSION_ENDED: WorkflowDefinition(
                name="SESSION_ENDED_FLOW",
                description="Triggered when session ends.",
                trigger_event=SystemEvent.SESSION_ENDED,
                stages=[WorkflowStage.POST_PROCESS]
            ),
            SystemEvent.MIDNIGHT_SYNC: WorkflowDefinition(
                name="MIDNIGHT_SYNC_FLOW",
                description="Triggered on midnight sync.",
                trigger_event=SystemEvent.MIDNIGHT_SYNC,
                stages=[WorkflowStage.POST_PROCESS]
            ),
            SystemEvent.RESOURCE_COMPLETED: WorkflowDefinition(
                name="RESOURCE_COMPLETED_FLOW",
                description="Triggered when resource is completed.",
                trigger_event=SystemEvent.RESOURCE_COMPLETED,
                stages=[WorkflowStage.CURATION]
            ),
            SystemEvent.WEEK_ENDED: WorkflowDefinition(
                name="WEEK_ENDED_FLOW",
                description="Triggered on week end.",
                trigger_event=SystemEvent.WEEK_ENDED,
                stages=[WorkflowStage.POST_PROCESS]
            ),
            SystemEvent.WEEK_STARTED: WorkflowDefinition(
                name="WEEK_STARTED_FLOW",
                description="Triggered on week start.",
                trigger_event=SystemEvent.WEEK_STARTED,
                stages=[WorkflowStage.PLANNING]
            ),
            SystemEvent.MONTH_STARTED: WorkflowDefinition(
                name="MONTH_STARTED_FLOW",
                description="Triggered on month start.",
                trigger_event=SystemEvent.MONTH_STARTED,
                stages=[WorkflowStage.PLANNING]
            ),
            SystemEvent.MONTH_ENDED: WorkflowDefinition(
                name="MONTH_ENDED_FLOW",
                description="Triggered on month end.",
                trigger_event=SystemEvent.MONTH_ENDED,
                stages=[WorkflowStage.POST_PROCESS]
            ),
            SystemEvent.APP_STARTED: WorkflowDefinition(
                name="APP_STARTED_FLOW",
                description="Triggered on app launch.",
                trigger_event=SystemEvent.APP_STARTED,
                stages=[WorkflowStage.PRE_PROCESS]
            ),
            SystemEvent.HABIT_UPDATED: WorkflowDefinition(
                name="HABIT_UPDATED_FLOW",
                description="Triggered on habit updates.",
                trigger_event=SystemEvent.HABIT_UPDATED,
                stages=[WorkflowStage.ANALYSIS]
            ),
        }

    def resolve(self, event_type: SystemEvent) -> WorkflowDefinition:
        """Resolves target workflow definitions from the system event.
        
        Args:
            event_type: Triggering system event type.
            
        Returns:
            WorkflowDefinition: Configured workflow description model.
            
        Raises:
            ValueError: If no workflow matches the event.
        """
        if event_type not in self._routes:
            raise ValueError(f"No configured workflow path found for event type: '{event_type.value}'.")
        return self._routes[event_type]
