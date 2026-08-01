from langgraph.graph import StateGraph, END
from app.ai.graph.state import LifeGPSState
from app.ai.graph.workflow import WorkflowStage
from app.infrastructure.logging.logger import logger

async def execute_stage_node(state: LifeGPSState, stage: WorkflowStage) -> LifeGPSState:
    """Generic node execution function for a specific WorkflowStage.
    
    This function delegates the actual agent execution to the ExecutionEngine
    fetched from the active dependency container.
    """
    logger.info("LangGraph executing stage node", stage=stage.value)
    # The ExecutionEngine will execute the active agent registered for this stage.
    # To avoid circular imports, the engine is accessed via container or context.
    from app.ai.runtime.container import container
    engine = container.engine
    
    # Run the engine execution for this stage
    updated_state = await engine.execute_stage(state, stage)
    return updated_state

def build_graph() -> StateGraph:
    """Assembles and compiles the stage-based LangGraph StateGraph.
    
    Returns:
        StateGraph: Compiled runnable LangGraph workflow.
    """
    builder = StateGraph(LifeGPSState)
    
    # 1. Register a node for every WorkflowStage
    for stage in WorkflowStage:
        # Bind the stage parameter to the generic execute function
        node_name = stage.value
        
        async def node_func(state: LifeGPSState, target_stage=stage) -> LifeGPSState:
            return await execute_stage_node(state, target_stage)
            
        builder.add_node(node_name, node_func)
        
    # 2. Add edges: connect each stage sequentially or back to the orchestrator.
    # For a dynamic stage flow, the execution engine runs the stages sequentially
    # according to the resolved WorkflowDefinition.
    # In LangGraph, we can define conditional edges or link stages.
    # Since the ExecutionEngine manages sequential stage execution internally or via a workflow sequence,
    # we can map the transition between nodes or simply set them up to exit to END.
    for stage in WorkflowStage:
        builder.add_edge(stage.value, END)
        
    builder.set_entry_point(WorkflowStage.PRE_PROCESS.value)
    
    logger.info("Compiled LangGraph StateGraph with Stage-based nodes.")
    return builder
