from app.ai.agents.planner.schemas import PlannerAgentOutput
from app.ai.framework.errors import ValidationError

class PlannerValidator:
    """Performs schedule boundary validations on the generated planner output agenda blocks."""

    def validate(self, output: PlannerAgentOutput) -> bool:
        """Runs validation rules.
        
        Args:
            output: PlannerAgentOutput to check.
            
        Returns:
            bool: True if passes validation rules.
            
        Raises:
            ValidationError: If criteria are failed.
        """
        # Ensure focus minutes has valid allocation
        if output.calendar_plan.total_focused_minutes < 0:
            raise ValidationError("Validation failed: calendar_plan total_focused_minutes cannot be negative.")
            
        # Verify event times are chronologically sequential
        for item in output.calendar_plan.agenda:
            if item.start_time >= item.end_time:
                raise ValidationError(f"Validation failed: event '{item.title}' start_time is after or equal to end_time.")
                
        return True
