from typing import List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class PlanningExplanation(BaseModel):
    """Explainability attributes documenting reasoning choices behind schedule slotting."""
    why_this_mission: str = Field(..., description="Justification for selecting this mission")
    why_this_time: str = Field(..., description="Justification for slotting this hour block")
    why_this_order: str = Field(..., description="Justification for execution priority ordering")
    supporting_gap: str = Field(..., description="Target gap being resolved")
    supporting_strategy: str = Field(..., description="Target strategy supporting planning decisions")
    expected_outcome: str = Field(..., description="Expected milestone outcome description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Planning confidence metric")
    deferred_reason: str = Field(default="Not deferred", description="Why this item was deferred, if applicable")
    skipped_risk: str = Field(..., description="The risk rating/explanation if this unit is skipped")
    alternative_schedule: str = Field(default="No alternative slot", description="Alternative calendar time suggested")

class PlanHealth(BaseModel):
    """Plan health metrics checked against behavioral capacities and prerequisites."""
    workload_balance: float = Field(..., ge=0.0, le=1.0, description="Overall workload balance rating")
    energy_match: float = Field(..., ge=0.0, le=1.0, description="Degree of alignment with daily energy curves")
    focus_match: float = Field(..., ge=0.0, le=1.0, description="Alignment with average focus span windows")
    dependency_integrity: float = Field(..., ge=0.0, le=1.0, description="Prerequisite dependency verification score")
    estimated_success_probability: float = Field(..., ge=0.0, le=1.0, description="Judges' metric showing probability of success")

class ExecutionPlanItem(BaseModel):
    """Refers to a specific ExecutionUnit allocated for completion."""
    unit_id: UUID = Field(..., description="ExecutionUnit ID")
    mission_id: UUID = Field(..., description="Parent mission ID")
    title: str = Field(..., description="Execution Unit title")
    estimated_duration: int = Field(..., description="Estimated effort in minutes")
    priority: float = Field(..., ge=0.0, le=1.0, description="Execution priority score")

class ExecutionPlan(BaseModel):
    """The linear checklist representing what units should be executed today."""
    target_date: str = Field(..., description="Target date YYYY-MM-DD")
    units_sequence: List[ExecutionPlanItem] = Field(default_factory=list, description="Ordered checklist items")
    health_score: PlanHealth = Field(..., description="Evaluated plan health indicator parameters")

class CalendarPlanItem(BaseModel):
    """An allocated execution unit scheduled in calendar time slots."""
    unit_id: UUID = Field(..., description="ExecutionUnit ID")
    title: str = Field(..., description="Execution Unit title")
    start_time: str = Field(..., description="ISO 8601 start timestamp")
    end_time: str = Field(..., description="ISO 8601 end timestamp")
    focus_window: str = Field(..., description="Window name (Morning, Afternoon, Evening)")
    explanation: PlanningExplanation = Field(..., description="Explainability trace")

class CalendarPlan(BaseModel):
    """The schedule mapping when daily tasks should occur."""
    target_date: str = Field(..., description="Target date YYYY-MM-DD")
    agenda: List[CalendarPlanItem] = Field(default_factory=list, description="Calendar time agenda slots")
    total_focused_minutes: int = Field(..., description="Sum of scheduled focused durations")
    breaks_count: int = Field(..., description="Inserted breaks count")
    recovery_slots_count: int = Field(..., description="Recovery slots count")

class PlannerAgentOutput(BaseModel):
    """The conformed output returned from the Planner Agent."""
    execution_plan: ExecutionPlan = Field(..., description="The Execution Plan details (WHAT)")
    calendar_plan: CalendarPlan = Field(..., description="The Calendar Plan details (WHEN)")
    weekly_objectives: List[str] = Field(default_factory=list, description="Stated goals for the week")
