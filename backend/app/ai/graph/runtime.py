from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.ai.graph.contracts import AgentResult

class ExecutionMetadata(BaseModel):
    """Observability metadata container tracking active LangGraph executions."""
    
    workflow_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the session run")
    execution_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the step execution")
    current_agent: str = Field("Orchestrator", description="The agent currently executing")
    completed_agents: List[str] = Field(default_factory=list, description="Agents that finished successfully")
    failed_agents: List[str] = Field(default_factory=list, description="Agents that encountered execution failures")
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time the execution started")
    execution_time: float = Field(0.0, description="Cumulative execution time in seconds")
    retry_count: int = Field(0, description="Active step retry count")
    trace_id: Optional[str] = Field(None, description="External trace logger identifier")

class RuntimeStepTracker(BaseModel):
    """Runtime tracker managing state evaluations across workflow steps."""
    
    metadata: ExecutionMetadata = Field(default_factory=ExecutionMetadata)
    steps_log: List[AgentResult] = Field(default_factory=list, description="Log of agent results executed in this run")
    
    def log_step(self, result: AgentResult) -> None:
        """Appends an agent result to the execution log and updates metadata.
        
        Args:
            result: Standardized AgentResult output.
        """
        self.steps_log.append(result)
        self.metadata.execution_time += result.execution_time
        
        if result.success:
            if result.agent_name not in self.metadata.completed_agents:
                self.metadata.completed_agents.append(result.agent_name)
        else:
            if result.agent_name not in self.metadata.failed_agents:
                self.metadata.failed_agents.append(result.agent_name)
                
        if result.next_agent:
            self.metadata.current_agent = result.next_agent
