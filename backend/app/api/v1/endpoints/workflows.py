from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Dict, Any, List
from datetime import datetime
from app.api.deps import get_current_user, get_db
from app.schemas.api import WorkflowRunRequest, WorkflowStatusResponse, WorkflowHistoryResponse
from app.models.user import User
from app.ai.runtime.container import container
from app.ai.runtime.engine import ExecutionEngine
from app.ai.graph.state import LifeGPSState
from app.ai.graph.router import WorkflowRouter
from app.ai.graph.events import SystemEvent

router = APIRouter()

# Global in-memory workflow execution status store
WORKFLOW_JOBS: Dict[UUID, Dict[str, Any]] = {}

async def run_async_workflow(
    workflow_id: UUID,
    state: LifeGPSState,
    event_type: SystemEvent,
    db: AsyncSession
):
    """Background task executing the sequential workflow steps and updating state cache."""
    try:
        # Build Router & Engine
        workflow_router = WorkflowRouter()
        workflow = workflow_router.resolve(event_type)
        engine = ExecutionEngine(container.registry)
        
        stages = workflow.stages
        total_stages = len(stages)
        
        # Initialize job cache values
        WORKFLOW_JOBS[workflow_id]["status"] = "running"
        WORKFLOW_JOBS[workflow_id]["decision_trace"].append(f"Resolved workflow '{workflow.name}' with {total_stages} stages.")
        
        for idx, stage in enumerate(stages):
            progress = (idx / total_stages) * 100.0
            WORKFLOW_JOBS[workflow_id]["completion_percentage"] = progress
            WORKFLOW_JOBS[workflow_id]["decision_trace"].append(f"Initiating workflow stage: {stage.name}")
            
            # Resolve target agent name
            try:
                agent = container.registry.resolve(stage)
                agent_name = agent.metadata.name
                WORKFLOW_JOBS[workflow_id]["current_agent"] = agent_name
            except Exception:
                agent_name = "None"
                WORKFLOW_JOBS[workflow_id]["decision_trace"].append(f"No agent registered for stage: {stage.name}")
            
            # Execute step
            state = await engine.execute_step(state, stage)
            
            # Sync logs back to cache
            WORKFLOW_JOBS[workflow_id]["completed_agents"] = list(state.execution.completed_agents)
            WORKFLOW_JOBS[workflow_id]["failed_agents"] = list(state.execution.failed_agents)
            WORKFLOW_JOBS[workflow_id]["errors"] = list(state.errors.errors)
            
            if state.errors.errors:
                WORKFLOW_JOBS[workflow_id]["decision_trace"].append(f"Stage {stage.name} reported validation errors.")
                break
                
        if WORKFLOW_JOBS[workflow_id]["errors"]:
            WORKFLOW_JOBS[workflow_id]["status"] = "failed"
        else:
            WORKFLOW_JOBS[workflow_id]["status"] = "completed"
            WORKFLOW_JOBS[workflow_id]["completion_percentage"] = 100.0
            
        WORKFLOW_JOBS[workflow_id]["decision_trace"].append(f"Workflow execution finished with status: {WORKFLOW_JOBS[workflow_id]['status']}.")
        WORKFLOW_JOBS[workflow_id]["completed_at"] = datetime.utcnow()
    except Exception as e:
        WORKFLOW_JOBS[workflow_id]["status"] = "failed"
        WORKFLOW_JOBS[workflow_id]["errors"].append(str(e))
        WORKFLOW_JOBS[workflow_id]["decision_trace"].append(f"Fatal executor error: {str(e)}")
        WORKFLOW_JOBS[workflow_id]["completed_at"] = datetime.utcnow()

@router.post("", response_model=WorkflowStatusResponse, status_code=status.HTTP_202_ACCEPTED, summary="Trigger a new workflow run")
async def trigger_workflow(
    request: WorkflowRunRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new workflow run, registers it in memory, and triggers background task execution."""
    try:
        event_enum = SystemEvent(request.event_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid event type name: {request.event_type}"
        )
        
    workflow_id = uuid4()
    
    # Initialize cache record
    WORKFLOW_JOBS[workflow_id] = {
        "workflow_id": workflow_id,
        "name": f"{event_enum.value}_FLOW",
        "trigger_event": event_enum.value,
        "status": "pending",
        "current_agent": "Orchestrator",
        "completed_agents": [],
        "failed_agents": [],
        "errors": [],
        "decision_trace": ["Triggered from REST API"],
        "completion_percentage": 0.0,
        "started_at": datetime.utcnow(),
        "completed_at": None,
        "user_id": current_user.id
    }
    
    # Prepare initial execution state
    state = LifeGPSState(
        event={"event_type": event_enum, "payload": request.payload},
        session={"session_id": uuid4(), "client_platform": "api"},
        user={"user_id": current_user.id}
    )
    state.metadata.workflow_id = workflow_id
    
    # Run the workflow task in the background
    background_tasks.add_task(run_async_workflow, workflow_id, state, event_enum, db)
    
    return WorkflowStatusResponse(**WORKFLOW_JOBS[workflow_id])

@router.get("/status/{workflow_id}", response_model=WorkflowStatusResponse, summary="Get status of active workflow")
async def get_workflow_status(workflow_id: UUID, current_user: User = Depends(get_current_user)):
    """Retrieves current execution progress, active agents, and traces for the specified workflow ID."""
    job = WORKFLOW_JOBS.get(workflow_id)
    if not job or job["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow job execution not found"
        )
    return WorkflowStatusResponse(**job)

@router.get("", response_model=list[WorkflowHistoryResponse], summary="Get workflow run history")
async def get_workflows_history(current_user: User = Depends(get_current_user)):
    """Returns the list of all historic workflow runs initiated by the user."""
    history = []
    for job in WORKFLOW_JOBS.values():
        if job["user_id"] == current_user.id:
            history.append(WorkflowHistoryResponse(
                workflow_id=job["workflow_id"],
                name=job["name"],
                trigger_event=job["trigger_event"],
                started_at=job["started_at"],
                completed_at=job["completed_at"],
                status=job["status"]
            ))
    return history
