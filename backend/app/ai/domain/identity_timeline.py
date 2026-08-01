from typing import List
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class IdentitySnapshot(BaseModel):
    """Domain model capturing a user's identity state at a specific point in time."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time of snapshot creation")
    identity_summary: str = Field(..., description="Summarized overview description of identity characteristics")
    goals: List[str] = Field(default_factory=list, description="User goals at snapshot time")
    interests: List[str] = Field(default_factory=list, description="User interests at snapshot time")
    skills: List[str] = Field(default_factory=list, description="Active skills catalog")
    reason_for_change: str = Field(..., description="Context explanation justifying identity changes")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in model assessment accuracy")
