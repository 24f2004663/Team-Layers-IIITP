from typing import Any, Dict, List
import time
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIResponse
from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.agents.identity.preprocessor import Preprocessor
from app.ai.agents.identity.context import IdentityContextBuilder
from app.ai.agents.identity.parser import IdentityParser
from app.ai.agents.identity.validator import IdentityValidator
from app.ai.agents.identity.memory import IdentityMemoryAdapter
from app.ai.agents.identity.timeline import TimelineHelper
from app.ai.framework.errors import ValidationError
from app.infrastructure.logging.logger import logger

class IdentityAgent(BaseAgent):
    """The Identity Agent analyzing onboarding properties to establish and evolve user archetype maps."""

    def __init__(self):
        # Configure self-describing AgentMetadata
        metadata = AgentMetadata(
            name="IdentityAgent",
            version="1.0.0",
            description="Analyzes user values and goals to determine who they want to become.",
            capabilities=["IDENTITY_ANALYSIS", "ARCHETYPE_EXTRACTION", "TIMELINE_EVOLUTION"],
            supported_events=[SystemEvent.USER_ONBOARDED, SystemEvent.PROFILE_UPDATED, SystemEvent.USER_LOGIN],
            required_memory=["identity"],
            stage=WorkflowStage.ANALYSIS,
            expected_output_schema="IdentityProfile",
            temperature=0.3,
            max_tokens=2048,
            recommended_model="gemini-1.5-pro"
        )
        super().__init__(metadata)
        
        # Instantiate adapters
        self.preprocessor = Preprocessor()
        self.context_builder = IdentityContextBuilder()
        self.parser = IdentityParser()
        self.validator = IdentityValidator(min_confidence=0.70)
        self.memory_adapter = IdentityMemoryAdapter()
        self.timeline_helper = TimelineHelper()

    async def initialize(self) -> None:
        logger.info("Initializing IdentityAgent")

    async def validate(self, state: LifeGPSState) -> bool:
        """Verifies if the trigger event type is supported.
        
        Args:
            state: The current LifeGPSState.
            
        Returns:
            bool: True if event is supported.
        """
        event_type = state.event.event_type
        if event_type not in self.metadata.supported_events:
            logger.warning(f"IdentityAgent skipped. Event '{event_type.value}' not supported.")
            return False
        return True

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Collects and compiles onboarding details from State.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Flattened variables dict for prompting.
        """
        raw_context = await self.preprocessor.preprocess(state, context)
        # Store raw context parameters in execution context metadata for downstream lifecycle steps
        context.metadata["raw_context"] = raw_context
        return self.context_builder.build_prompt_variables(raw_context)

    async def parse(self, response: AIResponse, context: ExecutionContext) -> IdentityProfile:
        """Parses raw text content into IdentityProfile schema models.
        
        Args:
            response: Input LLM response.
            context: ExecutionContext.
            
        Returns:
            IdentityProfile: Output parsed profile.
        """
        profile = self.parser.parse_profile(response)
        context.metadata["parsed_profile"] = profile
        return profile

    async def validate_output(self, parsed_output: IdentityProfile, context: ExecutionContext) -> bool:
        """Verifies confidence score and required field configurations.
        
        Args:
            parsed_output: Parsed IdentityProfile model.
            context: ExecutionContext.
            
        Returns:
            bool: True if valid.
        """
        return self.validator.validate(parsed_output)

    async def update_memory(self, parsed_output: IdentityProfile, state: LifeGPSState, context: ExecutionContext) -> None:
        """Saves conformed profile metrics and appends timeline snapshots.
        
        Args:
            parsed_output: Verified IdentityProfile.
            state: Active LifeGPSState.
            context: ExecutionContext.
        """
        # Save to database layer via memory adapter
        await self.memory_adapter.save_profile(state.user.user_id, parsed_output)
        
        # Build and append a timeline snapshot
        raw_context = context.metadata.get("raw_context", {})
        skills = raw_context.get("skills", [])
        goals = raw_context.get("goals", [])
        
        reason = "Onboarding completed"
        if state.event.event_type == SystemEvent.PROFILE_UPDATED:
            reason = "User profile update requested"
        elif state.event.event_type == SystemEvent.USER_LOGIN:
            reason = "Login status recalculation"
            
        snapshot = self.timeline_helper.create_snapshot(parsed_output, skills, goals, reason)
        await self.memory_adapter.append_snapshot(state, snapshot)
        
        # Update active state values
        state.identity.archetype = parsed_output.identity_summary
        state.identity.core_values = parsed_output.core_values
        state.identity.strengths = parsed_output.strengths
        state.identity.weaknesses = parsed_output.weaknesses

    async def postprocess(self, parsed_output: IdentityProfile, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        """Compiles final AgentResult including explanation schemas.
        
        Args:
            parsed_output: Final IdentityProfile.
            state: Active LifeGPSState.
            context: ExecutionContext.
            
        Returns:
            AgentResult: Conformed pipeline outcome.
        """
        # Build explainability payload
        explanation = {
            "summary": parsed_output.identity_summary,
            "reasoning": parsed_output.mission,
            "confidence": parsed_output.confidence_score,
            "memory_changes": {
                "archetype": parsed_output.identity_summary,
                "interests": parsed_output.interests
            },
            "timeline_changes": {
                "new_snapshot_timestamp": parsed_output.last_updated.isoformat(),
                "career_goal": parsed_output.career_goal
            }
        }
        
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary=f"Identity profile resolved for user {state.user.user_id}.",
            updated_fields=["identity.archetype", "identity.core_values", "identity.strengths", "identity.weaknesses"],
            execution_time=time.time() - context.started_at.timestamp(),
            confidence=parsed_output.confidence_score,
            explanation=explanation
        )

    async def cleanup(self) -> None:
        logger.info("IdentityAgent cleanup completed")
