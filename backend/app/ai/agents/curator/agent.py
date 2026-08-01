from typing import Any, Dict, List
import time
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIResponse
from app.ai.agents.curator.schemas import CuratorAgentOutput
from app.ai.agents.curator.preprocessor import Preprocessor
from app.ai.agents.curator.context import CuratorContextBuilder
from app.ai.agents.curator.prompt_builder import CuratorPromptBuilder
from app.ai.agents.curator.parser import CuratorParser
from app.ai.agents.curator.validator import CuratorValidator
from app.ai.agents.curator.memory import CuratorMemoryAdapter
from app.ai.agents.curator.timeline import CuratorTimelineHelper
from app.infrastructure.logging.logger import logger

class CuratorAgent(BaseAgent):
    """The Curator Agent composing personalized experience bundles for active execution tasks."""

    def __init__(self):
        metadata = AgentMetadata(
            name="CuratorAgent",
            version="1.2.0",
            description="Evaluates and ranks learning opportunities, structuring them as Experience Bundles.",
            capabilities=["EXPERIENCE_COMPOSITION", "PATH_OPTIMIZATION", "OPPORTUNITY_READINESS"],
            supported_events=[
                SystemEvent.USER_LOGIN,
                SystemEvent.TASK_COMPLETED,
                SystemEvent.RESOURCE_COMPLETED,
                SystemEvent.DAY_ENDED,
                SystemEvent.WEEK_ENDED,
                SystemEvent.PROFILE_UPDATED
            ],
            required_memory=["behavior", "identity"],
            stage=WorkflowStage.CURATION,
            expected_output_schema="CuratorAgentOutput",
            temperature=0.3,
            max_tokens=2048,
            recommended_model="gemini-1.5-pro"
        )
        super().__init__(metadata)
        
        self.preprocessor = Preprocessor()
        self.context_builder = CuratorContextBuilder()
        self.prompt_builder = CuratorPromptBuilder()
        self.parser = CuratorParser()
        self.validator = CuratorValidator()
        self.memory_adapter = CuratorMemoryAdapter()
        self.timeline_helper = CuratorTimelineHelper()

    async def initialize(self) -> None:
        logger.info("Initializing CuratorAgent")

    async def validate(self, state: LifeGPSState) -> bool:
        event_type = state.event.event_type
        supported_vals = [e.value for e in self.metadata.supported_events]
        if event_type not in self.metadata.supported_events and event_type.value not in supported_vals:
            logger.warning(f"CuratorAgent skipped. Event '{event_type.value}' not supported.")
            return False
        return True

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        raw_context = await self.preprocessor.preprocess(state, context)
        return self.context_builder.build_prompt_variables(raw_context)

    async def parse(self, response: AIResponse, context: ExecutionContext) -> CuratorAgentOutput:
        output = self.parser.parse_output(response)
        context.metadata["parsed_curator_output"] = output
        return output

    async def validate_output(self, parsed_output: CuratorAgentOutput, context: ExecutionContext) -> bool:
        return self.validator.validate(parsed_output)

    async def update_memory(self, parsed_output: CuratorAgentOutput, state: LifeGPSState, context: ExecutionContext) -> None:
        user_id = state.user.user_id
        await self.memory_adapter.save_bundle(user_id, parsed_output)
        
        # Append timeline snapshot
        snapshot = self.timeline_helper.create_snapshot(
            parsed_output.bundle.primary_video,
            parsed_output.bundle.expected_skill_gains,
            parsed_output.bundle.explanation.expected_learning_outcome
        )
        # Store snapshot to behavioral memory timeline
        from app.ai.runtime.container import container
        if container.behavior_memory:
            data = await container.behavior_memory.load(user_id)
            timeline_list = data.get("experiences_timeline", [])
            
            snap_dict = snapshot.model_dump()
            snap_dict["timestamp"] = snap_dict["timestamp"].isoformat()
            timeline_list.append(snap_dict)
            await container.behavior_memory.update(user_id, {"experiences_timeline": timeline_list})
            
        # Update state conformed attributes if any
        # No Curator modifications to state model are requested; it is read-only for scheduler outputs.

    async def postprocess(self, parsed_output: CuratorAgentOutput, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        explanation = {
            "summary": "Experience bundle curated successfully.",
            "relevance": parsed_output.bundle.quality_score.relevance,
            "path_order": parsed_output.bundle.path_order_sequence,
            "skills_gain": [g.model_dump() for g in parsed_output.bundle.expected_skill_gains],
            "why_this_resource": parsed_output.bundle.explanation.why_this_resource
        }
        
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary=f"Curation complete: video={parsed_output.bundle.primary_video}",
            updated_fields=[],
            execution_time=time.time() - context.started_at.timestamp(),
            confidence=0.95,
            explanation=explanation
        )

    async def cleanup(self) -> None:
        logger.info("CuratorAgent cleanup completed")
