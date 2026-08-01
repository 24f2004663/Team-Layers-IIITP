from typing import Any
from app.engines.learning_context.schemas import LearningContext
from app.engines.learning_context.builder import LearningContextBuilder
from app.engines.learning_context.validator import LearningContextValidator

class LearningContextEngine:
    """The central engine coordinating learning parameter normalization."""

    def __init__(self):
        self.builder = LearningContextBuilder()
        self.validator = LearningContextValidator()

    def generate_context(
        self,
        execution_unit: Any,
        identity: Any,
        behavior: Any,
        mission: Any
    ) -> LearningContext:
        """Assembles profiles and validates conformed learning parameters.
        
        Args:
            execution_unit: Current active ExecutionUnit.
            identity: IdentityProfile details.
            behavior: BehaviorProfile details.
            mission: Mission parent details.
            
        Returns:
            LearningContext: Validated learning context block.
        """
        ctx = self.builder.build_context(execution_unit, identity, behavior, mission)
        self.validator.validate(ctx)
        return ctx
