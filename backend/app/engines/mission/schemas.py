from typing import List, Optional
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class MissionStatus(str, Enum):
    """The lifecycle state machine of a growth mission."""
    CREATED = "CREATED"
    PLANNED = "PLANNED"
    SCHEDULED = "SCHEDULED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    REFLECTED = "REFLECTED"
    ARCHIVED = "ARCHIVED"

class ExecutionUnit(BaseModel):
    """A granular, actionable task block derived from a parent learning mission."""
    id: UUID = Field(default_factory=uuid4, description="Unique execution unit ID")
    mission_id: UUID = Field(..., description="Parent mission ID")
    title: str = Field(..., description="Granular task title")
    estimated_duration: int = Field(..., description="Estimated focus duration in minutes")
    required_energy: str = Field(..., description="Energy level needed (Low, Medium, High)")
    required_focus: str = Field(..., description="Focus level needed (Low, Medium, High)")
    dependencies: List[UUID] = Field(default_factory=list, description="Pre-requisite execution unit IDs")
    completion_criteria: List[str] = Field(default_factory=list, description="Metrics to mark unit complete")
    priority: float = Field(..., ge=0.0, le=1.0, description="Priority weight rating")

class Mission(BaseModel):
    """The granular, actionable target derived from Gap Analysis and Strategy layers."""

    mission_id: UUID = Field(default_factory=uuid4, description="Unique mission ID")
    title: str = Field(..., description="Descriptive mission title")
    objective: str = Field(..., description="Actionable learning objective target")
    description: str = Field(..., description="Detailed description")
    supporting_gap: str = Field(..., description="The Gap ID/Name this mission directly addresses")
    supporting_strategy: str = Field(..., description="The Growth Strategy strategy name mapped to this mission")
    success_criteria: List[str] = Field(default_factory=list, description="Measurable completion metrics")
    estimated_duration: int = Field(..., description="Estimated effort in minutes")
    difficulty: str = Field(..., description="Difficulty rating (Easy, Medium, Hard)")
    priority: float = Field(..., ge=0.0, le=1.0, description="Priority weight rating (0.0 to 1.0)")
    deadline: str = Field(..., description="ISO 8601 target completion date")
    energy_requirement: str = Field(..., description="Energy levels needed (Low, Medium, High)")
    focus_requirement: str = Field(..., description="Concentration focus level (Low, Medium, High)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Resolution confidence score")
    reasoning: str = Field(..., description="Justification statement mapping gaps and strategies to this specific target")
    status: MissionStatus = Field(default=MissionStatus.CREATED, description="Active status in mission lifecycle")
    execution_units: List[ExecutionUnit] = Field(default_factory=list, description="Granular task steps")
