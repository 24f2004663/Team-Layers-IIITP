from typing import Annotated, Any, Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from langchain_core.messages import BaseMessage
from app.ai.graph.events import SystemEvent

class MetadataSection(BaseModel):
    """Execution and system metadata for the state run."""
    workflow_id: UUID = Field(default_factory=uuid4, description="ID of the parent workflow execution")
    execution_id: UUID = Field(default_factory=uuid4, description="ID of the current step execution")
    trace_id: Optional[str] = Field(None, description="Observability trace link")
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Start timestamp of the execution")

class EventSection(BaseModel):
    """The event driving the active state run."""
    event_type: SystemEvent = Field(..., description="The type of system event trigger")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Metadata and context from the trigger event")

class SessionSection(BaseModel):
    """State regarding the user's active session."""
    session_id: UUID = Field(..., description="Active session ID")
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Last activity timestamp")
    client_platform: str = Field("unknown", description="Client operating system platform")

class UserSection(BaseModel):
    """Core basic user demographics and timezone configs."""
    user_id: UUID = Field(..., description="Unique user identifier")
    timezone: str = Field("UTC", description="Target local timezone")
    locale: str = Field("en_US", description="Target locale for content formatting")

class IdentitySection(BaseModel):
    """Personality profiling and character mapping (Managed by Identity Agent)."""
    core_values: List[str] = Field(default_factory=list, description="User defined principles")
    archetype: str = Field("Explorer", description="Derived user archetype")
    strengths: List[str] = Field(default_factory=list, description="Identified cognitive/actionable strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Target focus areas for growth")

class BehaviorSection(BaseModel):
    """Habits, behavioral analyses, and insights (Managed by Behavior Agent)."""
    habits: Dict[str, Any] = Field(default_factory=dict, description="Monitored habits and current streaks")
    cognitive_patterns: List[str] = Field(default_factory=list, description="Identified patterns (e.g. procrastination)")
    energy_levels: Dict[str, float] = Field(default_factory=dict, description="Time of day energy scores")

class GoalsSection(BaseModel):
    """Short and long term goals (Managed by Planner Agent)."""
    primary_focus: str = Field("", description="Main focus area for the current period")
    long_term_goals: List[Dict[str, Any]] = Field(default_factory=list, description="Multi-year goals and metrics")
    short_term_goals: List[Dict[str, Any]] = Field(default_factory=list, description="Immediate sprint goals")

class SkillsSection(BaseModel):
    """Identified, desired, and certified skills (Managed by Planner Agent)."""
    acquired_skills: List[str] = Field(default_factory=list, description="Skills verified as acquired")
    target_skills: List[str] = Field(default_factory=list, description="Skills target for roadmap plans")

class RoadmapSection(BaseModel):
    """The roadmap and sequence of milestones (Managed by Planner Agent)."""
    milestones: List[Dict[str, Any]] = Field(default_factory=list, description="Active milestones roadmap")
    current_milestone_id: Optional[str] = Field(None, description="The milestone currently active")

class DailyPlanSection(BaseModel):
    """Today's actionable task execution plan (Managed by Planner Agent)."""
    tasks: List[Dict[str, Any]] = Field(default_factory=list, description="List of tasks for the day")
    focus_time_slots: List[Dict[str, Any]] = Field(default_factory=list, description="Configured schedule allocations")

class RecommendationsSection(BaseModel):
    """Actionable materials, resources, and advice (Managed by Curator Agent)."""
    learning_resources: List[Dict[str, Any]] = Field(default_factory=list, description="Articles, exercises, and videos suggested")
    insights: List[str] = Field(default_factory=list, description="Micro-advice and conceptual reminders")

class ReflectionSection(BaseModel):
    """Daily/weekly reviews and cognitive logs (Managed by Reflection Agent)."""
    prompts: List[str] = Field(default_factory=list, description="Generated reflection questions for the user")
    responses: Dict[str, str] = Field(default_factory=dict, description="Answers matching the reflection prompts")
    synthesized_insight: str = Field("", description="Summarized cognitive patterns from reflection")

class ProgressSection(BaseModel):
    """Progress rates, scores, and metrics (Managed by Reflection Agent)."""
    growth_score: float = Field(0.0, description="Overall evaluated growth rating")
    milestone_completion_rate: float = Field(0.0, description="Completion percentage metric")
    habit_adherence: float = Field(0.0, description="Streak adherence percentage score")

class MemorySection(BaseModel):
    """References to saved facts, long-term indexes, and vector store keys."""
    semantic_keys: List[str] = Field(default_factory=list, description="Vector store identifiers for context search")
    session_keys: List[str] = Field(default_factory=list, description="Archived memory session reference keys")

class MessagesSection(BaseModel):
    """List of chat messages representing conversation history."""
    messages: List[BaseMessage] = Field(default_factory=list, description="Accumulated chat history")

class ExecutionSection(BaseModel):
    """Observability tracking within the graph run."""
    current_agent: str = Field("Orchestrator", description="The agent currently running node execution")
    completed_agents: List[str] = Field(default_factory=list, description="List of agents that completed successfully")
    failed_agents: List[str] = Field(default_factory=list, description="List of agents that failed during this run")
    retry_count: int = Field(0, description="Retry count of the current block execution")

class ErrorsSection(BaseModel):
    """Compilation of errors occurring during execution."""
    errors: List[str] = Field(default_factory=list, description="Collected warning and error stack logs")

class LifeGPSState(BaseModel):
    """The central runtime contract defining the shared state of the Life-GPS graph."""
    metadata: MetadataSection = Field(default_factory=MetadataSection)
    event: EventSection
    session: SessionSection
    user: UserSection
    identity: IdentitySection = Field(default_factory=IdentitySection)
    behavior: BehaviorSection = Field(default_factory=BehaviorSection)
    goals: GoalsSection = Field(default_factory=GoalsSection)
    skills: SkillsSection = Field(default_factory=SkillsSection)
    roadmap: RoadmapSection = Field(default_factory=RoadmapSection)
    daily_plan: DailyPlanSection = Field(default_factory=DailyPlanSection)
    recommendations: RecommendationsSection = Field(default_factory=RecommendationsSection)
    reflection: ReflectionSection = Field(default_factory=ReflectionSection)
    progress: ProgressSection = Field(default_factory=ProgressSection)
    memory: MemorySection = Field(default_factory=MemorySection)
    messages: MessagesSection = Field(default_factory=MessagesSection)
    execution: ExecutionSection = Field(default_factory=ExecutionSection)
    errors: ErrorsSection = Field(default_factory=ErrorsSection)
