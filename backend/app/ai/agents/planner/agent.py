from typing import Any, Dict, List
import time
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIResponse
from app.ai.agents.planner.schemas import PlannerAgentOutput
from app.ai.agents.planner.preprocessor import Preprocessor
from app.ai.agents.planner.context import PlannerContextBuilder
from app.ai.agents.planner.prompt_builder import PlannerPromptBuilder
from app.ai.agents.planner.parser import PlannerParser
from app.ai.agents.planner.validator import PlannerValidator
from app.ai.agents.planner.memory import PlannerMemoryAdapter
from app.ai.agents.planner.timeline import PlannerTimelineHelper
from app.infrastructure.logging.logger import logger

class PlannerAgent(BaseAgent):
    """The Planner Agent coordinating daily, weekly, and monthly schedule blueprints."""

    def __init__(self):
        metadata = AgentMetadata(
            name="PlannerAgent",
            version="1.1.0",
            description="Orchestrates daily checklists and calendar timesheets under energy/focus constraints.",
            capabilities=["ADAPTIVE_SCHEDULING", "CONFLICT_DETECTION", "BREAK_INSERTION", "PLAN_HEALTH_RATING"],
            supported_events=[
                SystemEvent.USER_LOGIN,
                SystemEvent.DAY_STARTED,
                SystemEvent.DAY_ENDED,
                SystemEvent.GOAL_UPDATED,
                SystemEvent.PROFILE_UPDATED
            ],
            required_memory=["behavior", "identity"],
            stage=WorkflowStage.PLANNING,
            expected_output_schema="PlannerAgentOutput",
            temperature=0.2,
            max_tokens=2048,
            recommended_model="gemini-1.5-pro"
        )
        super().__init__(metadata)
        
        self.preprocessor = Preprocessor()
        self.context_builder = PlannerContextBuilder()
        self.prompt_builder = PlannerPromptBuilder()
        self.parser = PlannerParser()
        self.validator = PlannerValidator()
        self.memory_adapter = PlannerMemoryAdapter()
        self.timeline_helper = PlannerTimelineHelper()

    async def initialize(self) -> None:
        logger.info("Initializing PlannerAgent")

    async def validate(self, state: LifeGPSState) -> bool:
        event_type = state.event.event_type
        supported_vals = [e.value for e in self.metadata.supported_events]
        extra_events = ["MISSION_COMPLETED"]
        if event_type not in self.metadata.supported_events and event_type.value not in supported_vals and event_type.value not in extra_events:
            logger.warning(f"PlannerAgent skipped. Event '{event_type.value}' not supported.")
            return False
        return True

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        raw_context = await self.preprocessor.preprocess(state, context)
        return self.context_builder.build_prompt_variables(raw_context)

    async def parse(self, response: AIResponse, context: ExecutionContext) -> PlannerAgentOutput:
        output = self.parser.parse_output(response)
        context.metadata["parsed_planner_output"] = output
        return output

    async def validate_output(self, parsed_output: PlannerAgentOutput, context: ExecutionContext) -> bool:
        return self.validator.validate(parsed_output)

    async def update_memory(self, parsed_output: PlannerAgentOutput, state: LifeGPSState, context: ExecutionContext) -> None:
        user_id = state.user.user_id
        await self.memory_adapter.save_plan(user_id, parsed_output)
        
        # Append timeline snapshot
        reason = f"Event trigger {state.event.event_type.value}"
        snapshot = self.timeline_helper.create_snapshot(
            parsed_output.calendar_plan.target_date,
            parsed_output.calendar_plan.total_focused_minutes,
            parsed_output.calendar_plan.agenda,
            reason
        )
        # Store snapshot to behavioral memory timeline
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            timeline_list = data.get("plans_timeline", [])
            
            snap_dict = snapshot.model_dump()
            snap_dict["timestamp"] = snap_dict["timestamp"].isoformat()
            timeline_list.append(snap_dict)
            await container.behavior_memory.update(user_id, {"plans_timeline": timeline_list})
            
        # Update conformed state attributes
        state.daily_plan.tasks = [
            {
                "task_id": str(item.unit_id),
                "title": item.title,
                "start_time": item.start_time,
                "end_time": item.end_time,
                "focus_window": item.focus_window
            }
            for item in parsed_output.calendar_plan.agenda
        ]

    async def postprocess(self, parsed_output: PlannerAgentOutput, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        explanation = {
            "summary": "Agenda scheduling compiled.",
            "health_score": parsed_output.execution_plan.health_score.model_dump(),
            "total_focused_minutes": parsed_output.calendar_plan.total_focused_minutes,
            "weekly_objectives": parsed_output.weekly_objectives,
            "agenda_explanations": [
                {
                    "title": item.title,
                    "why_this_time": item.explanation.why_this_time,
                    "expected_outcome": item.explanation.expected_outcome,
                    "skipped_risk": item.explanation.skipped_risk
                }
                for item in parsed_output.calendar_plan.agenda
            ]
        }
        
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary=f"Agenda compiled: {parsed_output.calendar_plan.total_focused_minutes} focus minutes scheduled.",
            updated_fields=["daily_plan.tasks"],
            execution_time=time.time() - context.started_at.timestamp(),
            confidence=0.95,
            explanation=explanation
        )

    async def cleanup(self) -> None:
        logger.info("PlannerAgent cleanup completed")
