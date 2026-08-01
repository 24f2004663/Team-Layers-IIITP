from typing import Dict
from pydantic import BaseModel, Field
from app.ai.prompts.base import PromptMetadata

class VersionedPrompt(BaseModel):
    """Container holding prompt metadata and raw template string content."""
    
    metadata: PromptMetadata = Field(..., description="Configuration metadata properties")
    template: str = Field(..., description="The raw uncompiled prompt string content")
