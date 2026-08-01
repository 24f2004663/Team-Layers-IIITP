from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIMessage, AIResponse

class AgentMetadata(BaseModel):
    """The configuration metadata declaring an Agent's capabilities and execution configurations."""
    name: str = Field(..., description="Unique name identifier of the agent")
    version: str = Field("1.0.0", description="Agent release version")
    description: str = Field(..., description="Short summary of what the agent does")
    capabilities: List[str] = Field(..., description="List of capabilities supported (e.g. IDENTITY_ANALYSIS)")
    supported_events: List[SystemEvent] = Field(..., description="SystemEvents the agent listens to")
    required_memory: List[str] = Field(..., description="List of memory layers required")
    priority: int = Field(0, description="Priority score resolving conflicts when matching stages")
    stage: WorkflowStage = Field(..., description="The standard workflow pipeline stage the agent operates in")
    expected_output_schema: Optional[str] = Field(None, description="String name representing expected schema")
    temperature: float = Field(0.3, description="Recommended model temperature")
    max_tokens: int = Field(2048, description="Maximum tokens budget limit")
    recommended_model: str = Field("gemini-1.5-pro", description="Recommended Gemini model variant")

class BaseAgent(ABC):
    """Abstract base class detailing the lifecycle and execution pipeline for all Life-GPS AI Agents."""

    def __init__(self, metadata: AgentMetadata):
        """Initializes the agent with metadata properties.
        
        Args:
            metadata: Configured AgentMetadata properties.
        """
        self.metadata = metadata

    @abstractmethod
    async def initialize(self) -> None:
        """Initializes internal dependencies, caches, or state values prior to execution."""
        raise NotImplementedError

    @abstractmethod
    async def validate(self, state: LifeGPSState) -> bool:
        """Validates whether the active state holds required sections for this agent's task.
        
        Args:
            state: The current LifeGPSState.
            
        Returns:
            bool: True if input constraints are met, False otherwise.
        """
        raise NotImplementedError

    # New Agent Lifecycle Hooks
    async def before_execute(self, state: LifeGPSState, context: ExecutionContext) -> None:
        """Hook executing before any preprocessing occurs."""
        pass

    async def preprocess(self, state: LifeGPSState, context: ExecutionContext) -> Dict[str, Any]:
        """Preprocesses variables and inputs required to build prompts.
        
        Returns:
            Dict[str, Any]: Flattened variables dict.
        """
        return {}

    async def before_llm(self, prompt: str, state: LifeGPSState, context: ExecutionContext) -> None:
        """Hook executing before the LLM invocation occurs."""
        pass

    async def call_llm(self, prompt: str, context: ExecutionContext) -> AIResponse:
        """Invokes LLM interface."""
        # This will be handled by AgentRuntime, sub-agents can override if required.
        raise NotImplementedError

    async def after_llm(self, response: AIResponse, state: LifeGPSState, context: ExecutionContext) -> None:
        """Hook executing immediately after the LLM returns a response."""
        pass

    async def parse(self, response: AIResponse, context: ExecutionContext) -> Any:
        """Parses output into structures."""
        return response.content

    async def validate_output(self, parsed_output: Any, context: ExecutionContext) -> bool:
        """Validates schema and business constraints for parsed outputs."""
        return True

    async def update_memory(self, parsed_output: Any, state: LifeGPSState, context: ExecutionContext) -> None:
        """Saves and updates memory frameworks."""
        pass

    async def postprocess(self, parsed_output: Any, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        """Postprocesses results into final AgentResult schemas."""
        raise NotImplementedError

    async def after_execute(self, state: LifeGPSState, context: ExecutionContext, result: AgentResult) -> None:
        """Hook executing after execution completes."""
        pass

    # Legacy execution fallback
    async def execute(self, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        """Standard legacy execute wrapper delegating execution to the platform's AgentRuntime."""
        from app.ai.runtime.container import container
        # Resolves runtime to handle execution using the new lifecycle pipeline
        return await container.agent_runtime.run(self, state, context)

    @abstractmethod
    async def cleanup(self) -> None:
        """Flushes temporary allocations or writes telemetry logs after execution."""
        raise NotImplementedError
