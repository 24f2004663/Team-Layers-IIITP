from typing import Any, Optional
from pydantic import BaseModel, Field

class LLMResponse(BaseModel):
    """Standardized response container returned by all LLM generate operations."""

    text: str = Field(..., description="The generated raw text response from the model")
    raw_response: Any = Field(None, description="The complete raw response object from the SDK client")
    prompt_tokens: int = Field(0, description="Tokens used in the prompt")
    completion_tokens: int = Field(0, description="Tokens used in the completion output")
    total_tokens: int = Field(0, description="Total tokens used")
    estimated_cost: float = Field(0.0, description="Estimated monetary cost of the call in USD")
