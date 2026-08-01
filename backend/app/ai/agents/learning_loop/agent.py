from typing import Any, Dict, List
import time
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIResponse
from app.ai.agents.learning_loop.schemas import LearningLoopAgentOutput
from app.ai.agents.learning_loop.preprocessor import Preprocessor
from app.ai.agents.learning_loop.context import LearningLoopContextBuilder
from app.ai.agents.learning_loop.prompt_builder import LearningLoopPromptBuilder
from app.ai.agents.learning_loop.parser import LearningLoopParser
from app.ai.agents.learning_loop.validator import LearningLoopValidator
from app.ai.agents.learning_loop.memory import LearningLoopMemoryAdapter
from app.ai.agents.learning_loop.timeline import LearningLoopTimelineHelper
from app.infrastructure.logging.logger import logger

class LearningLoopAgent(BaseAgent):
    """The Learning Loop Agent continuous learning engine of Life-GPS."""

    def __init__(self):
        metadata = AgentMetadata(
            name="LearningLoopAgent",
            version="1.3.0",
            description="Transforms execution performance evidence into reflections, growth deltas, and calibrations.",
            capabilities=["CAUSAL_REASONING", "COUNTERFACTUAL_ANALYSIS", "ADAPTIVE_INTERVENTIONS", "CALIBRATION"],
            supported_events=[
                SystemEvent.USER_LOGIN,
                SystemEvent.DAY_ENDED,
                SystemEvent.WEEK_ENDED,
                SystemEvent.REFLECTION_SUBMITTED,
                SystemEvent.PROFILE_UPDATED,
                SystemEvent.SESSION_ENDED,
                SystemEvent.USER_ONBOARDED
            ],
            required_memory=["behavior", "identity"],
            stage=WorkflowStage.ANALYSIS,
            expected_output_schema="LearningLoopAgentOutput",
            temperature=0.2,
            max_tokens=2048,
            recommended_model="gemini-1.5-pro"
        )
        super().__init__(metadata)
        
        self.preprocessor = Preprocessor()
        self.context_builder = LearningLoopContextBuilder()
        self.prompt_builder = LearningLoopPromptBuilder()
        self.parser = LearningLoopParser()
        self.validator = LearningLoopValidator()
        self.memory_adapter = LearningLoopMemoryAdapter()
        self.timeline_helper = LearningLoopTimelineHelper()

    async def initialize(self) -> None:
        logger.info("Initializing LearningLoopAgent")

    async def validate(self, state: LifeGPSState) -> bool:
        event_type = state.event.event_type
        supported_vals = [e.value for e in self.metadata.supported_events]
        if event_type not in self.metadata.supported_events and event_type.value not in supported_vals:
            logger.warning(f"LearningLoopAgent skipped. Event '{event_type.value}' not supported.")
            return False
        return True

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        raw_context = await self.preprocessor.preprocess(state, context)
        return self.context_builder.build_prompt_variables(raw_context)

    async def parse(self, response: AIResponse, context: ExecutionContext) -> LearningLoopAgentOutput:
        output = self.parser.parse_output(response)
        context.metadata["parsed_learning_loop_output"] = output
        return output

    async def validate_output(self, parsed_output: LearningLoopAgentOutput, context: ExecutionContext) -> bool:
        return self.validator.validate(parsed_output)

    async def update_memory(self, parsed_output: LearningLoopAgentOutput, state: LifeGPSState, context: ExecutionContext) -> None:
        user_id = state.user.user_id
        await self.memory_adapter.save_reflection(user_id, parsed_output)
        
        # Append timeline snapshot
        snapshot = self.timeline_helper.create_snapshot(
            parsed_output.growth_index.composite_index,
            parsed_output.weekly_trajectory.change_percentage,
            parsed_output.reflection.daily_reflection
        )
        # Store snapshot to behavioral memory growth timeline
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            timeline_list = data.get("growth_timeline", [])
            
            snap_dict = snapshot.model_dump()
            snap_dict["timestamp"] = snap_dict["timestamp"].isoformat()
            timeline_list.append(snap_dict)
            
            # Update Identity Evolution Graph history
            graph_history = data.get("identity_evolution_graph", [])
            for node in parsed_output.identity_graph.nodes:
                graph_history.append(node.model_dump())
                
            await container.behavior_memory.update(user_id, {
                "growth_timeline": timeline_list,
                "identity_evolution_graph": graph_history
            })

    async def postprocess(self, parsed_output: LearningLoopAgentOutput, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        explanation = {
            "summary": "Learning Loop reflections and calibrations compiled.",
            "growth_index": parsed_output.growth_index.composite_index,
            "weekly_trajectory": parsed_output.weekly_trajectory.model_dump(),
            "interventions": [i.model_dump() for i in parsed_output.interventions],
            "counterfactuals": [c.model_dump() for c in parsed_output.counterfactuals]
        }
        
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary=f"Reflections compiled: composite growth index={parsed_output.growth_index.composite_index}",
            updated_fields=[],
            execution_time=time.time() - context.started_at.timestamp(),
            confidence=0.95,
            explanation=explanation
        )

    async def cleanup(self) -> None:
        logger.info("LearningLoopAgent cleanup completed")
