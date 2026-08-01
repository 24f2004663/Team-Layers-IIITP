import time
from uuid import uuid4
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.graph.router import WorkflowRouter
from app.ai.graph.node_registry import NodeRegistry
from app.infrastructure.logging.logger import logger

class OrchestratorAgent:
    """The central coordinator managing state transitions and workflow sequencing."""

    def __init__(self, router: WorkflowRouter, registry: NodeRegistry):
        """Initializes the Orchestrator.
        
        Args:
            router: The active WorkflowRouter instance.
            registry: The NodeRegistry containing registered agent instances.
        """
        self.router = router
        self.registry = registry

    async def orchestrate(self, state: LifeGPSState) -> LifeGPSState:
        """Inspects the trigger event, plans execution, and runs nodes sequentially.
        
        Args:
            state: The current runtime LifeGPSState.
            
        Returns:
            LifeGPSState: The final modified state after workflow completion.
        """
        trigger = state.event.event_type
        logger.info("Orchestrator triggered", trigger_event=trigger, workflow_id=str(state.metadata.workflow_id))
        
        # Resolve target workflow
        try:
            workflow = self.router.resolve(trigger)
        except ValueError as err:
            logger.error("Workflow resolution failed", error=str(err))
            state.errors.errors.append(str(err))
            return state

        logger.info(f"Resolved workflow '{workflow.name}' with nodes: {workflow.nodes}")
        
        # Sequentially execute resolved nodes
        for node_name in workflow.nodes:
            state.execution.current_agent = node_name
            
            try:
                agent = self.registry.get_node(node_name)
            except KeyError:
                err_msg = f"Target node '{node_name}' not registered in NodeRegistry."
                logger.error(err_msg)
                state.errors.errors.append(err_msg)
                state.execution.failed_agents.append(node_name)
                break
                
            logger.info("Initializing node execution", node_name=node_name)
            start_time = time.time()
            
            try:
                await agent.initialize()
                
                # Validate state compatibility
                if not await agent.validate(state):
                    raise ValueError(f"State validation failed for agent '{node_name}'.")
                    
                # Run execution
                result: AgentResult = await agent.execute(state)
                elapsed = time.time() - start_time
                
                if result.success:
                    logger.info("Node execution succeeded", node_name=node_name, execution_time=elapsed)
                    state.execution.completed_agents.append(node_name)
                    # Apply changes or log details if necessary
                else:
                    raise RuntimeError(f"Agent '{node_name}' execution reported failure: {result.errors}")
                    
                await agent.cleanup()
                
            except Exception as e:
                logger.error("Node execution failed", node_name=node_name, error=str(e))
                state.errors.errors.append(str(e))
                state.execution.failed_agents.append(node_name)
                # Break flow execution on node failure
                break
                
        return state
