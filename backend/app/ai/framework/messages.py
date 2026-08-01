from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class AIMessage(BaseModel):
    """Unified container for all prompt and LLM message transactions."""

    role: str = Field(..., description="Role of the message author (e.g. system, user, assistant)")
    content: str = Field(..., description="Text content payload")
    attachments: List[Dict[str, Any]] = Field(default_factory=list, description="Associated file or media properties")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata parameters")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time recorded")

class AIResponse(BaseModel):
    """Standardized response container returned by all LLM interface implementations."""

    content: str = Field(..., description="The raw generated text content output")
    reasoning: Optional[str] = Field(None, description="Model inner monologue reasoning or chain of thought")
    structured_output: Optional[Any] = Field(None, description="Model parsed structured payload")
    token_usage: Dict[str, int] = Field(
        default_factory=lambda: {"prompt": 0, "completion": 0, "total": 0},
        description="Detailed token consumption"
    )
    latency: float = Field(0.0, description="Inference latency in seconds")
    cost: float = Field(0.0, description="Simulated monetary cost value")
    finish_reason: str = Field("stop", description="Model exit finish condition reason (e.g. stop, length)")
