from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Plaintext password")
    full_name: str = Field(..., description="User's full name")
    archetype: Optional[str] = Field("Explorer", description="Initial personality archetype")
    core_values: List[str] = Field(default_factory=list, description="Core life values")
    strengths: List[str] = Field(default_factory=list, description="Key personality strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Growth areas / weaknesses")

class UserLogin(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="Plaintext password")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT Access Token")
    refresh_token: str = Field(..., description="JWT Refresh Token")
    token_type: str = Field("bearer", description="Token type schema")

class UserResponse(BaseModel):
    id: UUID = Field(..., description="Unique User ID")
    email: str = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, description="Full Name")
    created_at: datetime = Field(..., description="Registration timestamp")

# --- Profile Schemas ---
class IdentityResponse(BaseModel):
    id: UUID
    user_id: UUID
    archetype: str
    core_values: List[str]
    strengths: List[str]
    weaknesses: List[str]

class BehaviorResponse(BaseModel):
    id: UUID
    user_id: UUID
    habits: Dict[str, Any]
    cognitive_patterns: List[str]
    energy_levels: Dict[str, float]

class GapAnalysisResponse(BaseModel):
    gap_description: str
    priority_score: float
    target_skills: List[str]
    urgency: str
    recommends_strategy: str

# --- Dashboard Schemas ---
class DashboardSummary(BaseModel):
    archetype: str
    overall_status: str = Field(..., description="Summary of current user status")
    active_goals_count: int
    completed_tasks_count: int
    composite_growth_index: float

class DashboardToday(BaseModel):
    current_mission: Optional[str] = Field(None, description="Active mission description")
    agenda: List[Dict[str, Any]] = Field(default_factory=list, description="Allocated calendar items for today")
    total_focused_minutes: int
    breaks_count: int

class DashboardProgress(BaseModel):
    completion_rate: float
    habits_adherence: float
    energy_levels: Dict[str, float]
    consistency_delta: float

class DashboardFuture(BaseModel):
    predicted_success_rate: float
    calibration_factor: float
    growth_trajectory_match: float
    recommended_interventions: List[str]

class DashboardFull(BaseModel):
    summary: DashboardSummary
    today: DashboardToday
    progress: DashboardProgress
    future: DashboardFuture

# --- Mission & Planner & Curator Schemas ---
class MissionResponse(BaseModel):
    mission_id: UUID
    title: str
    description: str
    priority: float
    target_skills: List[str]

class PlannerResponse(BaseModel):
    execution_plan: Dict[str, Any]
    calendar_plan: Dict[str, Any]
    weekly_objectives: List[str]

class CuratorResponse(BaseModel):
    bundle: Dict[str, Any]
    candidates_ranked: List[Dict[str, Any]]

# --- Reflection & Learning Loop Schemas ---
class ReflectionResponse(BaseModel):
    reflection: Dict[str, Any]
    quality_score: Dict[str, float]

class LearningLoopResponse(BaseModel):
    reflections: Dict[str, Any]
    growth_delta: Dict[str, float]
    causal_analyses: List[Dict[str, Any]]
    counterfactuals: List[Dict[str, Any]]
    growth_index: Dict[str, float]

# --- Workflow Schemas ---
class WorkflowRunRequest(BaseModel):
    event_type: str = Field(..., description="SystemEvent trigger type name")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event payload dictionary")

class WorkflowStatusResponse(BaseModel):
    workflow_id: UUID
    status: str
    current_agent: str
    completed_agents: List[str]
    failed_agents: List[str]
    errors: List[str]
    completion_percentage: float = 0.0

class WorkflowHistoryResponse(BaseModel):
    workflow_id: UUID
    name: str
    trigger_event: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str

# --- Demo Schemas ---
class DemoRunRequest(BaseModel):
    profile_name: str = Field(..., description="Demo profile to run (Student, Software Engineer, Founder, Career Switcher)")

class IdentityUpdate(BaseModel):
    archetype: Optional[str] = None
    core_values: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None

