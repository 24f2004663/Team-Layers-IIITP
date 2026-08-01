from typing import Any, Dict, List
import time
from datetime import datetime, timezone
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIResponse
from app.ai.agents.behavior.schemas import (
    BehaviorProfile, BehaviorObservation, BehaviorPattern, BehaviorEvidence,
    GrowthInsight, BehaviorAgentOutput
)
from app.ai.agents.behavior.preprocessor import Preprocessor
from app.ai.agents.behavior.context import BehaviorContextBuilder
from app.ai.agents.behavior.observation_extractor import ObservationExtractor
from app.ai.agents.behavior.evidence_engine import BehaviorEvidenceEngine
from app.ai.agents.behavior.pattern_analyzer import PatternAnalyzer
from app.ai.agents.behavior.drift_detector import BehaviorDriftDetector
from app.ai.agents.behavior.parser import BehaviorParser
from app.ai.agents.behavior.validator import BehaviorValidator
from app.ai.agents.behavior.memory import BehaviorMemoryAdapter
from app.ai.agents.behavior.timeline import BehaviorTimelineHelper
from app.ai.agents.behavior.metrics import GapAnalyzer, ConfidenceDecay
from app.ai.agents.identity.schemas import IdentityProfile
from app.infrastructure.logging.logger import logger

class BehaviorAgent(BaseAgent):
    """The Behavioral Intelligence Agent matching actions and evidence against targets."""

    def __init__(self):
        metadata = AgentMetadata(
            name="BehaviorAgent",
            version="1.1.0",
            description="Extracts observations and validates behavioral evidence gap alignments.",
            capabilities=["BEHAVIOR_DIAGNOSTIC", "PATTERN_SYNTHESIS", "ALIGNMENT_RATING", "DRIFT_DETECTOR"],
            supported_events=[
                SystemEvent.TASK_COMPLETED,
                SystemEvent.RESOURCE_COMPLETED,
                SystemEvent.DAY_ENDED,
                SystemEvent.WEEK_ENDED,
                SystemEvent.USER_LOGIN
            ],
            required_memory=["behavior", "identity"],
            stage=WorkflowStage.ANALYSIS,
            expected_output_schema="BehaviorAgentOutput",
            temperature=0.3,
            max_tokens=2048,
            recommended_model="gemini-1.5-pro"
        )
        super().__init__(metadata)
        
        self.extractor = ObservationExtractor()
        self.evidence_engine = BehaviorEvidenceEngine()
        self.pattern_analyzer = PatternAnalyzer()
        self.drift_detector = BehaviorDriftDetector()
        
        self.preprocessor = Preprocessor()
        self.context_builder = BehaviorContextBuilder()
        self.parser = BehaviorParser()
        self.validator = BehaviorValidator(min_confidence=0.70)
        self.memory_adapter = BehaviorMemoryAdapter()
        self.timeline_helper = BehaviorTimelineHelper()
        self.gap_analyzer = GapAnalyzer()
        self.decay_strategy = ConfidenceDecay(decay_rate_per_day=0.05)

    async def initialize(self) -> None:
        logger.info("Initializing BehaviorAgent")

    async def validate(self, state: LifeGPSState) -> bool:
        event_type = state.event.event_type
        # Allow string check fallback if enum type representation varies
        supported_vals = [e.value for e in self.metadata.supported_events]
        extra_events = ["TASK_SKIPPED", "RESOURCE_STARTED", "RESOURCE_ABANDONED", "GOAL_CHANGED", "SESSION_STARTED", "SESSION_ENDED"]
        if event_type not in self.metadata.supported_events and event_type.value not in supported_vals and event_type.value not in extra_events:
            logger.warning(f"BehaviorAgent skipped. Event '{event_type.value}' not supported.")
            return False
        return True

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        # 1. Extract new observation from current event
        new_obs = self.extractor.extract_observation(state.event.event_type, state.event.payload)
        
        # 2. Load existing observations and apply confidence decay
        raw_memory = await self.memory_adapter.load_profile(state.user.user_id)
        raw_obs_list = raw_memory.get("observations", [])
        
        observations = []
        for raw in raw_obs_list:
            try:
                obs = BehaviorObservation(**raw)
                # Apply decay
                obs.confidence = self.decay_strategy.calculate_decayed_confidence(
                    obs.confidence, obs.timestamp, datetime.now(timezone.utc)
                )
                observations.append(obs)
            except Exception as e:
                logger.warning("Failed to load historical observation", error=str(e))
                
        # Append the new observation
        observations.append(new_obs)
        
        # 3. Generate Evidence
        evidence = self.evidence_engine.generate_evidence(observations)
        
        # 4. Analyze Patterns
        patterns = self.pattern_analyzer.analyze_patterns(evidence)
        
        # Store resolved properties in context metadata for update step
        context.metadata["observations"] = observations
        context.metadata["evidence"] = evidence
        context.metadata["patterns"] = patterns
        context.metadata["baseline"] = raw_memory
        
        raw_context = await self.preprocessor.preprocess(state, context)
        return self.context_builder.build_prompt_variables(raw_context)

    async def parse(self, response: AIResponse, context: ExecutionContext) -> BehaviorProfile:
        profile = self.parser.parse_profile(response)
        context.metadata["parsed_profile"] = profile
        return profile

    async def validate_output(self, parsed_output: BehaviorProfile, context: ExecutionContext) -> bool:
        return self.validator.validate(parsed_output)

    async def update_memory(self, parsed_output: BehaviorProfile, state: LifeGPSState, context: ExecutionContext) -> None:
        user_id = state.user.user_id
        observations = context.metadata.get("observations", [])
        evidence = context.metadata.get("evidence", [])
        patterns = context.metadata.get("patterns", [])
        baseline = context.metadata.get("baseline", {})
        
        # Save to database memory layers
        await self.memory_adapter.save_profile(user_id, parsed_output)
        await self.memory_adapter.save_observations(user_id, observations)
        await self.memory_adapter.save_evidence(user_id, evidence)
        await self.memory_adapter.save_patterns(user_id, patterns)
        
        # Load Identity profile to run alignment calculation
        from app.ai.runtime.container import container
        identity_profile = None
        if container.identity_memory:
            id_data = await container.identity_memory.load(user_id)
            if id_data:
                try:
                    identity_profile = IdentityProfile(**id_data)
                except Exception:
                    pass
                    
        if not identity_profile:
            identity_profile = IdentityProfile(
                identity_summary="Seed Identity Goals",
                career_goal="Professional Developer",
                mission="Growth focus",
                core_values=["Growth"],
                interests=["Python"],
                strengths=["Logic"],
                weaknesses=[],
                confidence_score=0.9
            )
            
        alignment, growth_insights = self.gap_analyzer.analyze_gaps(identity_profile, parsed_output)
        context.metadata["alignment"] = alignment
        context.metadata["growth_insights"] = growth_insights
        
        # Behavior Drift Detection
        drift_warnings = self.drift_detector.detect_drift(parsed_output, baseline)
        context.metadata["drift_warnings"] = drift_warnings
        
        # Append timeline snapshot
        reason = f"Event trigger {state.event.event_type.value}"
        snapshot = self.timeline_helper.create_snapshot(parsed_output, patterns, reason)
        await self.memory_adapter.append_snapshot(state, snapshot)
        context.metadata["timeline_snapshot"] = snapshot
        
        # Update conformed fields on state
        state.behavior.cognitive_patterns = [pat.pattern_name for pat in patterns]
        state.behavior.habits["consistency_score"] = parsed_output.consistency_score
        state.behavior.habits["alignment_score"] = alignment.alignment_score
        state.behavior.energy_levels["motivation"] = 1.0 if parsed_output.motivation_level.lower() == "high" else 0.5

    async def postprocess(self, parsed_output: BehaviorProfile, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        alignment = context.metadata.get("alignment")
        observations = context.metadata.get("observations", [])
        evidence = context.metadata.get("evidence", [])
        patterns = context.metadata.get("patterns", [])
        growth_insights = context.metadata.get("growth_insights", [])
        snapshot = context.metadata.get("timeline_snapshot")
        drift_warnings = context.metadata.get("drift_warnings", [])
        
        # Assemble BehaviorAgentOutput
        agent_output = BehaviorAgentOutput(
            profile=parsed_output,
            observations=observations,
            evidence=evidence,
            patterns=patterns,
            alignment=alignment,
            growth_insights=growth_insights,
            timeline_snapshot=snapshot
        )
        
        explanation = {
            "summary": f"Behavior profile calculated for user {state.user.user_id}.",
            "reasoning": alignment.reasoning if alignment else "Calculated behavioral profile attributes.",
            "confidence": parsed_output.confidence_score,
            "agent_output": agent_output.model_dump(mode="json"),
            "drift_warnings": [w.model_dump() for w in drift_warnings]
        }
        
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary=f"Behavioral tracking compiled. Alignment is {int(alignment.alignment_score * 100 if alignment else 100)}%.",
            updated_fields=["behavior.cognitive_patterns", "behavior.habits", "behavior.energy_levels"],
            execution_time=time.time() - context.started_at.timestamp(),
            confidence=parsed_output.confidence_score,
            explanation=explanation
        )

    async def cleanup(self) -> None:
        logger.info("BehaviorAgent cleanup completed")
