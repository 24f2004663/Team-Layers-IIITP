from typing import Any
from app.engines.learning_context.schemas import LearningContext

class LearningContextBuilder:
    """Collects and merges execution units, identities, and behaviors into a conformed LearningContext."""

    def build_context(
        self,
        execution_unit: Any,
        identity: Any,
        behavior: Any,
        mission: Any
    ) -> LearningContext:
        """Assembles profiles and targets into a conformed schema.
        
        Args:
            execution_unit: Current active ExecutionUnit.
            identity: IdentityProfile details.
            behavior: BehaviorProfile details.
            mission: Mission parent details.
            
        Returns:
            LearningContext: Assembled conformed context.
        """
        # Resolve duration limits
        duration = getattr(execution_unit, "estimated_duration", 30)
        
        # Format style to support expanded categories
        base_style = getattr(behavior, "learning_style", "Project-Based") if hasattr(behavior, "learning_style") else "Project-Based"
        if base_style not in ["Visual", "Project-Based", "Reading", "Interactive", "Research", "Discussion"]:
            base_style = "Project-Based"
            
        return LearningContext(
            topic=getattr(mission, "title", "General study"),
            subtopics=[getattr(execution_unit, "title", "Practice")],
            required_skills=getattr(identity, "strengths", []),
            missing_skills=getattr(identity, "weaknesses", []),
            difficulty=getattr(execution_unit, "difficulty", "Medium") if hasattr(execution_unit, "difficulty") else "Medium",
            preferred_learning_style=base_style,
            available_time=duration,
            energy_level=getattr(behavior, "motivation_level", "Medium") if hasattr(behavior, "motivation_level") else "Medium",
            attention_span=getattr(behavior, "attention_span_minutes", 30) if hasattr(behavior, "attention_span_minutes") else 30,
            prerequisites=[],
            learning_goal=getattr(mission, "objective", "Gain base skill competence")
        )
