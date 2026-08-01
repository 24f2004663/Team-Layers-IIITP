from datetime import datetime, timezone
from pydantic import BaseModel, Field

class PromptMetadata(BaseModel):
    """The configuration metadata detailing template attributes, authors, and model configurations."""

    name: str = Field(..., description="The name of the prompt template")
    version: str = Field("v1", description="Version identifier string (e.g. v1)")
    description: str = Field(..., description="Summary details on what the template accomplishes")
    author: str = Field("System", description="Author of the template")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time created")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time updated")
    supported_agent: str = Field(..., description="Target AI agent name")
    supported_model: str = Field("gemini-1.5-pro", description="Target recommended model")
