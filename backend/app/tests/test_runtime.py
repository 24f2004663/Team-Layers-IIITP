import pytest
from uuid import uuid4
from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.graph.workflow import WorkflowStage, WorkflowDefinition
from app.ai.graph.router import WorkflowRouter
from app.ai.graph.agent_registry import AgentRegistry
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.contracts import AgentResult
from app.ai.runtime.context import ExecutionContext
from app.ai.runtime.engine import ExecutionEngine
from app.ai.graph.builder import build_graph

class FakeAgent(BaseAgent):
    """Mock agent implementation for runtime tests."""

    async def initialize(self) -> None:
        pass

    async def validate(self, state: LifeGPSState) -> bool:
        return True

    async def execute(self, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        context.trace.append(f"FakeAgent executed inside {context.current_stage.value}")
        return AgentResult(
            success=True,
            agent_name=self.metadata.name,
            summary="FakeAgent execution successful.",
            updated_fields=["metadata.execution_id"],
            execution_time=0.01,
            confidence=0.95
        )

    async def cleanup(self) -> None:
        pass

@pytest.fixture
def test_registry() -> AgentRegistry:
    """Fixture providing a configured AgentRegistry with mock agents."""
    registry = AgentRegistry()
    
    # 1. Register Pre-Process Agent
    pre_agent = FakeAgent(
        AgentMetadata(
            name="MockPreAgent",
            description="Mock Pre-process",
            capabilities=["MOCK_PRE"],
            supported_events=[SystemEvent.USER_LOGIN],
            required_memory=[],
            stage=WorkflowStage.PRE_PROCESS
        )
    )
    registry.register(pre_agent)
    
    # 2. Register Analysis Agent
    analysis_agent = FakeAgent(
        AgentMetadata(
            name="MockAnalysisAgent",
            description="Mock Analysis",
            capabilities=["MOCK_ANALYSIS"],
            supported_events=[SystemEvent.USER_LOGIN],
            required_memory=[],
            stage=WorkflowStage.ANALYSIS
        )
    )
    registry.register(analysis_agent)
    
    return registry

def test_workflow_router():
    """Verifies that the router resolves triggers into target stage sequences."""
    router = WorkflowRouter()
    workflow = router.resolve(SystemEvent.USER_LOGIN)
    assert workflow.name == "USER_LOGIN_FLOW"
    assert WorkflowStage.PRE_PROCESS in workflow.stages
    assert WorkflowStage.ANALYSIS in workflow.stages

def test_agent_registry(test_registry: AgentRegistry):
    """Verifies agent registration, listing, and stage resolution."""
    assert test_registry.validate()
    assert "MockPreAgent" in test_registry.list()
    assert "MOCK_PRE" in test_registry.capabilities()
    
    resolved = test_registry.resolve(WorkflowStage.PRE_PROCESS)
    assert resolved.metadata.name == "MockPreAgent"

def test_graph_builder(test_registry: AgentRegistry):
    """Verifies that the build_graph compiles cleanly."""
    graph = build_graph()
    assert graph is not None

@pytest.mark.asyncio
async def test_execution_engine(test_registry: AgentRegistry):
    """Verifies sequential workflow execution and middleware interception."""
    engine = ExecutionEngine(test_registry)
    
    # Setup state
    state = LifeGPSState(
        event={"event_type": SystemEvent.USER_LOGIN, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    workflow = WorkflowDefinition(
        name="TEST_WORKFLOW",
        description="Test workflow run",
        trigger_event=SystemEvent.USER_LOGIN,
        stages=[WorkflowStage.PRE_PROCESS, WorkflowStage.ANALYSIS]
    )
    
    # Run workflow
    final_state = await engine.run_workflow(state, workflow)
    
    assert "MockPreAgent" in final_state.execution.completed_agents
    assert "MockAnalysisAgent" in final_state.execution.completed_agents
    assert not final_state.execution.failed_agents
    assert not final_state.errors.errors
