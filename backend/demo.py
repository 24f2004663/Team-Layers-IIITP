import json
import os
import asyncio
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.graph.workflow import WorkflowStage, WorkflowDefinition
from app.ai.runtime.engine import ExecutionEngine
from app.ai.runtime.container import container
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory

async def run_demo():
    print("==================================================")
    print("           Life-GPS Agentic OS Demo               ")
    print("==================================================")
    
    # Load demo user
    demo_file = os.path.join(os.path.dirname(__file__), "demo", "student.json")
    with open(demo_file, "r") as f:
        user_data = json.load(f)
        
    print(f"Loaded demo profile: {user_data['name']} ({user_data['archetype']})")
    print(f"Target Career Goal: {user_data['identity']['career_goal']}")
    print(f"Focus Style: {user_data['behavior']['focus_style']}")
    
    # Setup mock LLM response
    mock_llm = MagicMock()
    
    async def side_effect(messages, *args, **kwargs):
        mock_responses = {
            "IdentityAgent": '{"identity_summary": "CS Student", "career_goal": "Engineer", "mission": "Learn code", "core_values": ["growth"], "interests": ["python"], "strengths": ["logic"], "weaknesses": ["experience"], "learning_style": "Visual", "preferred_difficulty": "Medium", "time_commitment": "5 hours/week", "motivation_level": "High", "confidence_score": 0.9, "last_updated": "2026-08-01T09:00:00Z"}',
            "BehaviorAgent": '{"learning_style": "Visual", "focus_style": "Spurt", "attention_span_minutes": 30, "productive_hours": [9, 10], "preferred_session_length": 45, "procrastination_level": "Low", "consistency_score": 0.8, "adaptability_score": 0.7, "motivation_level": "Medium", "energy_pattern": "High", "stress_pattern": "Stable", "confidence_score": 0.9, "last_updated": "2026-08-01T09:00:00Z"}',
            "GapAnalysisAgent": '{"gap_description": "Lack programming", "priority_score": 0.8, "target_skills": ["python"], "urgency": "High", "recommends_strategy": "Intensive"}',
        }
        target_json = mock_responses["IdentityAgent"]
        prompt_str = str(messages)
        for agent_name, resp_json in mock_responses.items():
            if agent_name in prompt_str or agent_name.lower() in prompt_str.lower():
                target_json = resp_json
                break
        return AIResponse(
            content=target_json,
            latency=0.01,
            cost=0.0001,
            finish_reason="stop"
        )
        
    mock_llm.invoke = AsyncMock(side_effect=side_effect)
    llm_factory.get_llm = lambda provider: mock_llm

    # Setup state
    state = LifeGPSState(
        event={"event_type": SystemEvent.USER_LOGIN, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": user_data["user_id"]}
    )
    
    # Build engine
    engine = ExecutionEngine(container.registry)
    
    # Define Demo Workflow stage pipeline
    demo_workflow = WorkflowDefinition(
        name="DEMO_FLOW",
        description="Demo workflow run for hackathon showcase",
        trigger_event=SystemEvent.USER_LOGIN,
        stages=[WorkflowStage.ANALYSIS]
    )
    
    print("\nRunning Agentic OS Workflow stages sequentially...")
    final_state = await engine.run_workflow(state, demo_workflow)
    
    print("\n================ Workflow Completed ================")
    print(f"Status: Success")
    print(f"Completed Agents: {final_state.execution.completed_agents}")
    print("==================================================\n")

if __name__ == "__main__":
    asyncio.run(run_demo())
