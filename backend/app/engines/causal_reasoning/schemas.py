from typing import List
from pydantic import BaseModel, Field

class CauseAnalysis(BaseModel):
    """Causal mapping explaining the root behavior driver behind logged outcomes."""

    root_cause: str = Field(..., description="Identified root cause explanation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Causal inference confidence score")
    evidence: List[str] = Field(default_factory=list, description="Supporting behaviors observed")
    recommended_intervention: str = Field(..., description="Suggested corrective action suggestion")
