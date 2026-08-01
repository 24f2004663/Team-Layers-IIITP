from pydantic import BaseModel, Field

class OutcomeAnalysis(BaseModel):
    """Calculated outcomes evaluating user progress success and behavior shifts."""

    mission_success_rate: float = Field(..., ge=0.0, le=1.0, description="Mission success rate (0.0 to 1.0)")
    learning_success_rate: float = Field(..., ge=0.0, le=1.0, description="Concept comprehension success rate")
    skill_gain_ratio: float = Field(..., ge=0.0, description="Skill value adjustment ratio")
    consistency_gain_ratio: float = Field(..., description="Consistency metric delta")
    behavior_change_indicator: float = Field(..., description="Calculated behavioral adaptation score")
    identity_progress_score: float = Field(..., ge=0.0, le=1.0, description="Identity alignment progress score")
