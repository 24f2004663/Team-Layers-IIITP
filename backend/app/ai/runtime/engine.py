import time
from typing import Callable, List, Dict, Any, Awaitable
from uuid import uuid4
from datetime import datetime, timezone
from app.ai.graph.state import LifeGPSState
from app.ai.graph.workflow import WorkflowStage, WorkflowDefinition
from app.ai.graph.contracts import AgentResult
from app.ai.graph.agent_registry import AgentRegistry
from app.ai.runtime.context import ExecutionContext
from app.infrastructure.logging.logger import logger

# Type definition for middleware callables
MiddlewareCallable = Callable[
    [LifeGPSState, ExecutionContext, Callable[[LifeGPSState, ExecutionContext], Awaitable[AgentResult]]],
    Awaitable[AgentResult]
]

class LoggingMiddleware:
    """Middleware executing logging hooks around agent execution runs."""
    
    async def __call__(
        self, 
        state: LifeGPSState, 
        context: ExecutionContext, 
        next_call: Callable[[LifeGPSState, ExecutionContext], Awaitable[AgentResult]]
    ) -> AgentResult:
        logger.info("LoggingMiddleware: Pre-agent run", agent=context.current_agent, stage=context.current_stage.value)
        context.trace.append(f"Started agent {context.current_agent} in stage {context.current_stage.value}")
        
        result = await next_call(state, context)
        
        logger.info("LoggingMiddleware: Post-agent run", agent=context.current_agent, success=result.success)
        context.trace.append(f"Finished agent {context.current_agent} (Success: {result.success})")
        return result

class ValidationMiddleware:
    """Middleware enforcing validation checks prior to agent logic execution."""
    
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        
    async def __call__(
        self, 
        state: LifeGPSState, 
        context: ExecutionContext, 
        next_call: Callable[[LifeGPSState, ExecutionContext], Awaitable[AgentResult]]
    ) -> AgentResult:
        logger.info("ValidationMiddleware: Verifying state validation", agent=context.current_agent)
        # Fetch target agent from registry to check validator compatibility
        agent = self.registry.resolve(context.current_stage)
        
        if not await agent.validate(state):
            logger.error("ValidationMiddleware: State validation failed!", agent=context.current_agent)
            return AgentResult(
                success=False,
                agent_name=context.current_agent,
                summary="State validation failed.",
                errors=["Pre-execution state validation check returned False."],
                execution_time=0.0,
                confidence=0.0
            )
            
            
        return await next_call(state, context)

class MemoryMiddleware:
    """Middleware saving and loading context memory records dynamically."""
    
    async def __call__(
        self, 
        state: LifeGPSState, 
        context: ExecutionContext, 
        next_call: Callable[[LifeGPSState, ExecutionContext], Awaitable[AgentResult]]
    ) -> AgentResult:
        logger.info("MemoryMiddleware: Loading memory layer triggers", agent=context.current_agent)
        # Perform execution
        result = await next_call(state, context)
        
        logger.info("MemoryMiddleware: Syncing updated outputs to persistent layers", agent=context.current_agent)
        return result

class MetricsMiddleware:
    """Middleware tracking run latency, token costs, and scoring metrics."""
    
    async def __call__(
        self, 
        state: LifeGPSState, 
        context: ExecutionContext, 
        next_call: Callable[[LifeGPSState, ExecutionContext], Awaitable[AgentResult]]
    ) -> AgentResult:
        start_time = time.time()
        result = await next_call(state, context)
        elapsed = time.time() - start_time
        
        # Accumulate metrics
        context.cost += 0.0015  # Simulated cost increment
        context.token_usage["prompt"] += 120
        context.token_usage["completion"] += 80
        context.token_usage["total"] += 200
        
        logger.info("MetricsMiddleware: Logged step metrics", agent=context.current_agent, latency_s=elapsed)
        return result


class ExecutionEngine:
    """The core engine pipeline running workflow stages through configured middlewares and registry agents."""

    def __init__(self, registry: AgentRegistry):
        """Initializes the ExecutionEngine.
        
        Args:
            registry: The active AgentRegistry instance.
        """
        self.registry = registry
        # Configure middleware pipeline
        self.middlewares: List[MiddlewareCallable] = [
            LoggingMiddleware(),
            MetricsMiddleware(),
            MemoryMiddleware(),
            ValidationMiddleware(self.registry)
        ]

    async def execute_stage(self, state: LifeGPSState, stage: WorkflowStage) -> LifeGPSState:
        """Executes a single workflow stage, resolving the target agent and invoking middlewares.
        
        Args:
            state: The active LifeGPSState.
            stage: The target WorkflowStage to execute.
            
        Returns:
            LifeGPSState: The updated LifeGPSState.
        """
        try:
            agent = self.registry.resolve(stage)
        except ValueError as e:
            logger.warning("No agent resolved for stage, skipping step execution", stage=stage.value, error=str(e))
            return state
            
        agent_name = agent.metadata.name
        
        # Construct ExecutionContext for this stage
        context = ExecutionContext(
            workflow_id=state.metadata.workflow_id,
            execution_id=uuid4(),
            event=state.event.event_type,
            current_stage=stage,
            current_agent=agent_name,
            completed_agents=state.execution.completed_agents,
            failed_agents=state.execution.failed_agents
        )
        
        # Build middleware chain ending at agent.execute
        async def root_executor(s: LifeGPSState, ctx: ExecutionContext) -> AgentResult:
            await agent.initialize()
            res = await agent.execute(s, ctx)
            await agent.cleanup()
            return res
            
        # Compose pipeline recursively
        chain = root_executor
        for middleware in reversed(self.middlewares):
            # Create closure to capture the current state of chain
            def make_step(mw=middleware, next_step=chain):
                async def step(s: LifeGPSState, ctx: ExecutionContext) -> AgentResult:
                    return await mw(s, ctx, next_step)
                return step
            chain = make_step()
            
        # Execute the chain
        result = await chain(state, context)
        
        # Map result back to state execution logs
        if result.success:
            state.execution.completed_agents.append(agent_name)
        else:
            state.execution.failed_agents.append(agent_name)
            state.errors.errors.extend(result.errors)
            
        return state

    async def run_workflow(self, state: LifeGPSState, workflow: WorkflowDefinition) -> LifeGPSState:
        """Runs a complete WorkflowDefinition stage-by-stage sequentially.
        
        Args:
            state: The active LifeGPSState.
            workflow: Configured WorkflowDefinition.
            
        Returns:
            LifeGPSState: Final modified state.
        """
        logger.info("Starting sequential execution for workflow definition", workflow_name=workflow.name)
        state.metadata.start_time = datetime.now(timezone.utc)
        
        for stage in workflow.stages:
            state = await self.execute_stage(state, stage)
            # Stop sequence on failure
            if state.execution.failed_agents:
                logger.error("Workflow execution halted due to stage failure", stage=stage.value)
                break
                
        return state
