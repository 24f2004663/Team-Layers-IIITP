from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from uuid import UUID
from app.api.v1.endpoints.workflows import WORKFLOW_JOBS
from app.infrastructure.logging.logger import logger

router = APIRouter()

@router.websocket("/ws/workflow")
async def websocket_workflow_stream(websocket: WebSocket):
    """WebSocket endpoint streaming progress, active agent, and decision trace updates for a workflow."""
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        # Step 1: Wait for client to send the target workflow_id
        data = await websocket.receive_text()
        try:
            payload = json.loads(data)
            workflow_id_str = payload.get("workflow_id")
            workflow_id = UUID(workflow_id_str)
        except Exception as e:
            await websocket.send_text(json.dumps({"error": f"Invalid workflow_id payload: {str(e)}"}))
            await websocket.close()
            return
            
        logger.info("WebSocket client subscribed to workflow", workflow_id=workflow_id)
        
        last_percentage = -1.0
        last_status = ""
        last_trace_len = 0
        
        # Step 2: Stream loop periodically reading from the global WORKFLOW_JOBS cache
        while True:
            job = WORKFLOW_JOBS.get(workflow_id)
            if not job:
                await websocket.send_text(json.dumps({"error": f"Workflow {workflow_id} not found."}))
                await asyncio.sleep(2.0)
                continue
                
            current_percentage = job.get("completion_percentage", 0.0)
            current_status = job.get("status", "pending")
            current_trace = job.get("decision_trace", [])
            
            # Only send update if progress, status, or trace logs have changed
            if (current_percentage != last_percentage or 
                current_status != last_status or 
                len(current_trace) != last_trace_len):
                
                update_payload = {
                    "workflow_id": str(workflow_id),
                    "status": current_status,
                    "current_agent": job.get("current_agent", "Orchestrator"),
                    "completed_agents": job.get("completed_agents", []),
                    "failed_agents": job.get("failed_agents", []),
                    "completion_percentage": current_percentage,
                    "decision_trace": current_trace,
                    "errors": job.get("errors", [])
                }
                await websocket.send_text(json.dumps(update_payload))
                
                last_percentage = current_percentage
                last_status = current_status
                last_trace_len = len(current_trace)
                
            # If the job completed or failed, we can terminate after one last confirmation
            if current_status in ["completed", "failed"]:
                logger.info("WebSocket workflow job finished. Ending stream.", workflow_id=workflow_id)
                break
                
            await asyncio.sleep(0.5)
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected. Channel closed.")
    except Exception as e:
        logger.error("Error during WebSocket execution loop", error=str(e))
        try:
            await websocket.close()
        except Exception:
            pass
