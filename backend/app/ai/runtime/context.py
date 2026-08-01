from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage

class ExecutionContext(BaseModel):
    """The runtime tracking context passed to every agent executing inside a stage."""

    workflow_id: UUID = Field(default_factory=uuid4, description="Unique ID of the parent workflow")
    execution_id: UUID = Field(default_factory=uuid4, description="Unique ID of the active run step")
    event: SystemEvent = Field(..., description="The event that triggered the runtime run")
    current_stage: WorkflowStage = Field(..., description="The active workflow stage")
    current_agent: str = Field(..., description="The name of the agent executing the stage")
    completed_agents: List[str] = Field(default_factory=list, description="List of successful agent nodes")
    failed_agents: List[str] = Field(default_factory=list, description="List of failed agent nodes")
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time execution started")
    ended_at: Optional[datetime] = Field(None, description="Time execution completed")
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt": 0, "completion": 0, "total": 0})
    cost: float = Field(0.0, description="Estimated monetary cost of execution")
    warnings: List[str] = Field(default_factory=list, description="Execution warning logs")
    trace: List[str] = Field(default_factory=list, description="Step trace logs for observability")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata arguments")
