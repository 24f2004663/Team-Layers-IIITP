from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.ai.graph.events import SystemEvent

class WorkflowStage(str, Enum):
    """The standardized pipeline stages for Life-GPS agentic execution."""
    PRE_PROCESS = "PRE_PROCESS"
    ANALYSIS = "ANALYSIS"
    PLANNING = "PLANNING"
    KNOWLEDGE = "KNOWLEDGE"
    CURATION = "CURATION"
    POST_PROCESS = "POST_PROCESS"
    MEMORY_UPDATE = "MEMORY_UPDATE"

class WorkflowDefinition(BaseModel):
    """Configuration mapping a SystemEvent trigger to ordered execution WorkflowStages."""
    
    name: str = Field(..., description="Unique workflow name identifier")
    description: str = Field(..., description="Description of the workflow goal")
    trigger_event: SystemEvent = Field(..., description="The SystemEvent key triggering the workflow")
    stages: List[WorkflowStage] = Field(..., description="Ordered list of execution stages")
    retry_policy: Optional[Dict[str, Any]] = Field(None, description="Retry configuration for stages")
    timeout: Optional[float] = Field(None, description="Max execution timeout in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata parameters")
