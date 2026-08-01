from pydantic import BaseModel, Field

class ExecutionEvidence(BaseModel):
    """Accumulated evidence representing actual user execution performance and focus trends."""

    completed_missions_count: int = Field(..., ge=0, description="Total completed missions count")
    completed_execution_units: int = Field(..., ge=0, description="Total completed task blocks count")
    session_duration_minutes: int = Field(..., ge=0, description="Combined study session time in minutes")
    interruptions_count: int = Field(..., ge=0, description="Total logged task interruptions count")
    mood_value: str = Field(..., description="Self-reported user mood")
    energy_level: str = Field(..., description="Self-reported energy state (Low, Medium, High)")
    error_logs_count: int = Field(..., ge=0, description="Count of execution error indicators logged")
    user_feedback_score: float = Field(..., ge=0.0, le=1.0, description="Aggregated user satisfaction score")
