from typing import Any, Dict, List
import time
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIResponse
from app.ai.agents.gap_analysis.schemas import GapAnalysisResult
from app.ai.agents.gap_analysis.preprocessor import Preprocessor
from app.ai.agents.gap_analysis.context import GapContextBuilder
from app.ai.agents.gap_analysis.prompt_builder import GapPromptBuilder
from app.ai.agents.gap_analysis.parser import GapParser
from app.ai.agents.gap_analysis.validator import GapValidator
from app.ai.agents.gap_analysis.memory import GapMemoryAdapter
from app.infrastructure.logging.logger import logger

class GapAnalysisAgent(BaseAgent):
    """The Gap Analysis Agent diagnosing aspiration and metric differences."""

    def __init__(self):
        metadata = AgentMetadata(
            name="GapAnalysisAgent",
            version="1.0.0",
            description="Compares target aspiration values against behavioral performance traits.",
            capabilities=["GAP_DIAGNOSIS", "ALIGNMENT_AUDIT", "TRACEABLE_DECISIONS"],
            supported_events=[
                SystemEvent.PROFILE_UPDATED,
                SystemEvent.GOAL_UPDATED,
                SystemEvent.WEEK_ENDED,
                SystemEvent.MONTH_ENDED,
                SystemEvent.USER_LOGIN
            ],
            required_memory=["behavior", "identity"],
            stage=WorkflowStage.ANALYSIS,
            expected_output_schema="GapAnalysisResult",
            temperature=0.2,
            max_tokens=2048,
            recommended_model="gemini-1.5-pro"
        )
        super().__init__(metadata)
        
        self.preprocessor = Preprocessor()
        self.context_builder = GapContextBuilder()
        self.prompt_builder = GapPromptBuilder()
        self.parser = GapParser()
        self.validator = GapValidator()
        self.memory_adapter = GapMemoryAdapter()

    async def initialize(self) -> None:
        logger.info("Initializing GapAnalysisAgent")

    async def validate(self, state: LifeGPSState) -> bool:
        event_type = state.event.event_type
        supported_vals = [e.value for e in self.metadata.supported_events]
        if event_type not in self.metadata.supported_events and event_type.value not in supported_vals:
            logger.warning(f"GapAnalysisAgent skipped. Event '{event_type.value}' not supported.")
            return False
        return True

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        raw_context = await self.preprocessor.preprocess(state, context)
        return self.context_builder.build_prompt_variables(raw_context)

    async def parse(self, response: AIResponse, context: ExecutionContext) -> GapAnalysisResult:
        result = self.parser.parse_result(response)
        context.metadata["parsed_gap_result"] = result
        return result

    async def validate_output(self, parsed_output: GapAnalysisResult, context: ExecutionContext) -> bool:
        return self.validator.validate(parsed_output)

    async def update_memory(self, parsed_output: GapAnalysisResult, state: LifeGPSState, context: ExecutionContext) -> None:
        user_id = state.user.user_id
        await self.memory_adapter.save_gap_result(user_id, parsed_output)
        
        # Run Decision Engine priorities resolution
        from app.ai.agents.gap_analysis.decision_engine import DecisionEngine
        engine = DecisionEngine()
        decision = engine.resolve_priorities(parsed_output)
        context.metadata["decision_priority"] = decision
        
        # Update conformed state attributes
        state.errors.errors.append(f"Gaps identified: overall gap score is {parsed_output.overall_gap_score}")

    async def postprocess(self, parsed_output: GapAnalysisResult, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        decision = context.metadata.get("decision_priority")
        explanation = {
            "summary": "Gap Analysis completed.",
            "overall_gap_score": parsed_output.overall_gap_score,
            "recommended_strategy": parsed_output.recommended_strategy,
            "decision_trace": parsed_output.decision_trace.model_dump(),
            "decision_priority": decision.model_dump() if decision else {}
        }
        
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary=f"Gap Diagnosis evaluated: score is {parsed_output.overall_gap_score}.",
            updated_fields=["errors.errors"],
            execution_time=time.time() - context.started_at.timestamp(),
            confidence=parsed_output.confidence,
            explanation=explanation
        )

    async def cleanup(self) -> None:
        logger.info("GapAnalysisAgent cleanup completed")
