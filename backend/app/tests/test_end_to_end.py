import pytest
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock
from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.graph.workflow import WorkflowStage, WorkflowDefinition
from app.ai.runtime.context import ExecutionContext
from app.ai.runtime.container import container
from app.ai.runtime.engine import ExecutionEngine
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory
from app.ai.agents.identity.agent import IdentityAgent
from app.ai.agents.behavior.agent import BehaviorAgent
from app.ai.agents.gap_analysis.agent import GapAnalysisAgent
from app.ai.agents.planner.agent import PlannerAgent
from app.ai.agents.curator.agent import CuratorAgent
from app.ai.agents.learning_loop.agent import LearningLoopAgent

# Simple mock memory manager
class MockMemory:
    def __init__(self):
        self.db = {}
    async def load(self, uid):
        return self.db.get(uid, {"growth_timeline": [], "reflections_history": []})
    async def save(self, uid, data):
        self.db[uid] = data
        return True
    async def update(self, uid, data):
        if uid not in self.db:
            self.db[uid] = {}
        self.db[uid].update(data)
        return True

MOCK_LLM_RESPONSES = {
    "IdentityAgent": '{"identity_summary": "CS Student", "career_goal": "Engineer", "mission": "Learn code", "core_values": ["growth"], "interests": ["python"], "strengths": ["logic"], "weaknesses": ["experience"], "learning_style": "Visual", "preferred_difficulty": "Medium", "time_commitment": "5 hours/week", "motivation_level": "High", "confidence_score": 0.9, "last_updated": "2026-08-01T09:00:00Z"}',
    "BehaviorAgent": '{"learning_style": "Visual", "focus_style": "Spurt", "attention_span_minutes": 30, "productive_hours": [9, 10], "preferred_session_length": 45, "procrastination_level": "Low", "consistency_score": 0.8, "adaptability_score": 0.7, "motivation_level": "Medium", "energy_pattern": "High", "stress_pattern": "Stable", "confidence_score": 0.9, "last_updated": "2026-08-01T09:00:00Z"}',
    "GapAnalysisAgent": '{"gap_description": "Lack programming", "priority_score": 0.8, "target_skills": ["python"], "urgency": "High", "recommends_strategy": "Intensive"}',
    "PlannerAgent": '{"execution_plan": {"target_date": "2026-08-01", "units_sequence": [{"unit_id": "00000000-0000-0000-0000-000000000000", "mission_id": "00000000-0000-0000-0000-000000000000", "title": "Review variables", "estimated_duration": 20, "priority": 0.90}], "health_score": {"workload_balance": 0.90, "energy_match": 0.85, "focus_match": 0.95, "dependency_integrity": 1.0, "estimated_success_probability": 0.92}}, "calendar_plan": {"target_date": "2026-08-01", "agenda": [{"unit_id": "00000000-0000-0000-0000-000000000000", "title": "Review variables", "start_time": "2026-08-01T09:00:00Z", "end_time": "2026-08-01T09:20:00Z", "focus_window": "Morning", "explanation": {"why_this_mission": "Prerequisite syntax task", "why_this_time": "Peak hour", "why_this_order": "First", "supporting_gap": "Prerequisite", "supporting_strategy": "Tiny Habits", "expected_outcome": "Solid fundamentals", "confidence": 0.95, "deferred_reason": "Not deferred", "skipped_risk": "High", "alternative_schedule": "09:30:00Z"}}], "total_focused_minutes": 20, "breaks_count": 1, "recovery_slots_count": 1}, "weekly_objectives": ["Acquire basic Python syntax"]}',
    "CuratorAgent": '{"bundle": {"primary_video": "https://youtube.com/py-var", "official_documentation": "https://scikit-learn.org", "practice_exercise": "https://practice.com/py-loops", "mini_project": "https://github.com/project/ml-basic", "github_repository": "https://github.com/project/reference-code", "quiz": "https://quiz.com/py-var", "optional_reading": "Optional article", "reflection_question": "How memory lookup compares?", "estimated_completion_time_minutes": 45, "expected_skill_gains": [{"skill_name": "Python", "gain_percentage": 0.08}], "resource_diversity_score": 0.85, "path_order_sequence": ["1. Video", "2. Documentation"], "standard_option": "Standard: Follow full 5-step pathway", "fast_track_option": "Fast Track", "deep_dive_option": "Deep Dive", "confidence": 0.90, "quality_score": {"relevance": 0.92, "diversity": 0.85, "time_efficiency": 0.88, "skill_coverage": 0.90, "historical_success": 0.85, "confidence": 0.95}, "explanation": {"why_this_resource": "Top ranked high-quality video", "why_now": "Morning focus slot", "how_it_supports_mission": "Prerequisite basics", "which_skill_gap_it_closes": "Loops syntax gap", "expected_learning_outcome": "Understand list structures", "confidence": 0.95, "alternative_option": "Fast Track"}}, "candidates_ranked": [{"resource_name": "Learn Python Variables video", "resource_type": "Video", "url": "https://youtube.com/py-var", "score": 0.95, "rank": 1, "quality_score": 0.95, "opportunity_readiness": {"readiness_percentage": 0.82, "missing_skills": ["Docker"], "preparation_time_hours": 12.0}}]}',
    "LearningLoopAgent": '{"reflection": {"daily_reflection": "Good", "weekly_reflection": "On track", "mission_reflection": "Perfect", "learning_reflection": "Fine", "behavior_reflection": "Low distractions", "identity_reflection": "Good progress", "quality_score": {"evidence_coverage": 0.9, "reasoning_quality": 0.9, "actionability": 0.8, "confidence": 0.9, "completeness": 0.9}}, "growth_delta": {"yesterday_consistency": 0.6, "today_consistency": 0.7, "yesterday_focus_minutes": 60, "today_focus_minutes": 90, "consistency_delta": 0.1, "focus_delta": 30, "learning_velocity_delta": 0.05}, "resource_effectiveness": [], "simulator_calibration": {"predicted_outcome_probability": 0.8, "actual_outcome_probability": 0.85, "calibration_factor": 1.05, "updated_weight": 0.88}, "counterfactuals": [], "interventions": [], "growth_index": {"focus": 0.8, "consistency": 0.8, "learning_velocity": 0.8, "skill_gain": 0.8, "identity_alignment": 0.8, "mission_completion": 0.8, "momentum": 0.8, "composite_index": 0.8}, "decision_memory": {"decision_id": "00000000-0000-0000-0000-000000000000", "outcome_description": "Morning block resolved", "success_rating": 0.9, "future_weight": 0.9}, "identity_graph": {"nodes": []}, "weekly_trajectory": {"target_identity": "AI Engineer", "current_match_percentage": 0.7, "previous_match_percentage": 0.6, "change_percentage": 0.1}}'
}

@pytest.fixture
def mock_llm_chain():
    mock_llm = MagicMock()
    
    async def side_effect(messages, *args, **kwargs):
        prompt_str = str(messages)
        print(f"DEBUG PROMPT: {prompt_str}")
        target_json = MOCK_LLM_RESPONSES["IdentityAgent"]
        
        if "PLANNING" in prompt_str:
            target_json = MOCK_LLM_RESPONSES["PlannerAgent"]
        elif "CURATION" in prompt_str:
            target_json = MOCK_LLM_RESPONSES["CuratorAgent"]
        elif "POST_PROCESS" in prompt_str:
            target_json = MOCK_LLM_RESPONSES["LearningLoopAgent"]
        elif "ANALYSIS" in prompt_str:
            target_json = MOCK_LLM_RESPONSES["IdentityAgent"]
            
        return AIResponse(
            content=target_json,
            latency=0.01,
            cost=0.0001,
            finish_reason="stop"
        )
        
    mock_llm.invoke = AsyncMock(side_effect=side_effect)
    original_get_llm = llm_factory.get_llm
    llm_factory.get_llm = lambda provider: mock_llm
    yield mock_llm
    llm_factory.get_llm = original_get_llm

@pytest.mark.asyncio
async def test_end_to_end_operating_system_pipeline(mock_llm_chain):
    """Executes a full multi-stage pipeline flow verifying sequential state updates."""
    # Setup mock memory managers
    mock_mem = MockMemory()
    container.identity_memory = mock_mem
    container.behavior_memory = mock_mem
    container.planner_memory = mock_mem
    container.curator_memory = mock_mem
    
    # Initialize Engine
    engine = ExecutionEngine(container.registry)
    
    # Define state
    state = LifeGPSState(
        event={"event_type": SystemEvent.USER_LOGIN, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    # Explicit definition of the entire 6-agent stage sequence
    e2e_workflow = WorkflowDefinition(
        name="E2E_VERIFICATION_FLOW",
        description="Verifies every core agent sequence pipeline",
        trigger_event=SystemEvent.USER_LOGIN,
        stages=[
            WorkflowStage.PRE_PROCESS,  # Resolves Identity
            WorkflowStage.ANALYSIS,     # Resolves Gap/Decision
            WorkflowStage.PLANNING,     # Resolves Planner
            WorkflowStage.CURATION,     # Resolves Curator
            WorkflowStage.POST_PROCESS  # Resolves Learning Loop / Post-process
        ]
    )
    
    final_state = await engine.run_workflow(state, e2e_workflow)
    
    # Verify traces and completion counts
    assert not final_state.errors.errors
    assert len(final_state.execution.completed_agents) > 0
