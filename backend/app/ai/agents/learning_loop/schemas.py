from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class CounterfactualScenario(BaseModel):
    """A what-if scenario predicting what outcome changes would result from behavior changes."""
    change: str = Field(..., description="Actionable change condition (e.g. +20 mins focus)")
    expected_delta: float = Field(..., description="Projected success probability delta (rate)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Counterfactual confidence")

class Intervention(BaseModel):
    """An adaptive, corrective recommendation triggered by negative behavioral trends."""
    trigger: str = Field(..., description="Behavioral trigger (e.g. Sleep drop)")
    recommendation: str = Field(..., description="Actionable corrective suggestion (e.g. screen downtime)")
    expected_effect: float = Field(..., ge=0.0, le=1.0, description="Projected outcome improvement rate")
    priority: float = Field(..., ge=0.0, le=1.0, description="Intervention priority score")

class PersonalGrowthIndex(BaseModel):
    """Flagship composite metric scoring overall progress across multiple dimensions."""
    focus: float = Field(..., ge=0.0, le=1.0, description="Attention span rating")
    consistency: float = Field(..., ge=0.0, le=1.0, description="Streak consistency rating")
    learning_velocity: float = Field(..., ge=0.0, le=1.0, description="Concept velocity rating")
    skill_gain: float = Field(..., ge=0.0, le=1.0, description="Aggregate skill gain rate")
    identity_alignment: float = Field(..., ge=0.0, le=1.0, description="Aspirations alignment score")
    mission_completion: float = Field(..., ge=0.0, le=1.0, description="Mission completed fraction")
    momentum: float = Field(..., ge=0.0, le=1.0, description="Sprint momentum score")
    composite_index: float = Field(..., ge=0.0, le=1.0, description="Final Personal Growth Index rating")

class ResourceEffectivenessMatrix(BaseModel):
    """Multidimensional effectiveness matrix scoring resource types across key criteria."""
    resource_type: str = Field(..., description="Type (Video, Docs, Practice, Project, Quiz)")
    learning_gain: float = Field(..., ge=0.0, le=1.0, description="Knowledge gain rating")
    retention: float = Field(..., ge=0.0, le=1.0, description="Comprehension retention rating")
    completion: float = Field(..., ge=0.0, le=1.0, description="Resource completion rate")
    enjoyment: float = Field(..., ge=0.0, le=1.0, description="User enjoyment rating")

class DecisionMemory(BaseModel):
    """A record logging recommendation decisions and actual performance outcomes."""
    decision_id: UUID = Field(default_factory=uuid4, description="Unique decision ID")
    outcome_description: str = Field(..., description="Result outcome overview")
    success_rating: float = Field(..., ge=0.0, le=1.0, description="Success factor score")
    future_weight: float = Field(..., ge=0.0, le=1.0, description="Recalculated decision weight multiplier")

class IdentityEvolutionGraphNode(BaseModel):
    """A state node representing the user's career/target identity at a specific point in time."""
    state_name: str = Field(..., description="Identity state target name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Transition confidence")
    transition_timestamp: str = Field(..., description="ISO 8601 transition timestamp")

class IdentityEvolutionGraph(BaseModel):
    """The graph mapping the chronological evolution of the user's career/target identity."""
    nodes: List[IdentityEvolutionGraphNode] = Field(default_factory=list, description="Chronological nodes list")

class ReflectionQualityScore(BaseModel):
    """Evaluates the comprehensiveness and actionability of generated reflections."""
    evidence_coverage: float = Field(..., ge=0.0, le=1.0, description="Coverage score")
    reasoning_quality: float = Field(..., ge=0.0, le=1.0, description="Reasoning score")
    actionability: float = Field(..., ge=0.0, le=1.0, description="Intervention actionability score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Evaluation confidence")
    completeness: float = Field(..., ge=0.0, le=1.0, description="Completeness score")

class WeeklyLifeTrajectory(BaseModel):
    """Weekly trajectory comparing target identity alignment progress."""
    target_identity: str = Field(..., description="Target career identity")
    current_match_percentage: float = Field(..., ge=0.0, le=1.0, description="Current week match score")
    previous_match_percentage: float = Field(..., ge=0.0, le=1.0, description="Previous week match score")
    change_percentage: float = Field(..., description="Change rate delta (positive/negative)")

class ReflectionReport(BaseModel):
    """The conformed Reflection Report."""
    daily_reflection: str = Field(..., description="Daily summary")
    weekly_reflection: str = Field(..., description="Weekly trends analysis")
    mission_reflection: str = Field(..., description="Aspirations progress review")
    learning_reflection: str = Field(..., description="Concepts comprehension review")
    behavior_reflection: str = Field(..., description="Focus habits review")
    identity_reflection: str = Field(..., description="Identity alignment review")
    quality_score: ReflectionQualityScore = Field(..., description="Evaluated quality metrics")

class GrowthDelta(BaseModel):
    """Calculated performance delta indicators tracking day-over-day changes."""
    yesterday_consistency: float = Field(..., description="Previous consistency score")
    today_consistency: float = Field(..., description="Current consistency score")
    yesterday_focus_minutes: int = Field(..., description="Previous focus duration")
    today_focus_minutes: int = Field(..., description="Current focus duration")
    consistency_delta: float = Field(..., description="Calculated difference value")
    focus_delta: float = Field(..., description="Focus minutes difference value")
    learning_velocity_delta: float = Field(..., description="Calculated velocity rate delta adjustment")

class SimulatorCalibration(BaseModel):
    """Calibration outcomes comparing predicted vs actual outcomes."""
    predicted_outcome_probability: float = Field(..., ge=0.0, le=1.0, description="Simulation prediction score")
    actual_outcome_probability: float = Field(..., ge=0.0, le=1.0, description="Actual outcome performance score")
    calibration_factor: float = Field(..., description="Adjusted multiplier")
    updated_weight: float = Field(..., ge=0.0, le=1.0, description="Updated confidence weight factor")

class LearningLoopAgentOutput(BaseModel):
    """The conformed output model returned by the Learning Loop Agent."""
    reflection: ReflectionReport = Field(..., description="Reflection report")
    growth_delta: GrowthDelta = Field(..., description="Calculated growth parameters")
    resource_effectiveness: List[ResourceEffectivenessMatrix] = Field(default_factory=list, description="Multidimensional resource matrix")
    simulator_calibration: SimulatorCalibration = Field(..., description="Calibration values")
    counterfactuals: List[CounterfactualScenario] = Field(default_factory=list, description="What-if scenarios")
    interventions: List[Intervention] = Field(default_factory=list, description="Corrective actions")
    growth_index: PersonalGrowthIndex = Field(..., description="Composite growth rating index")
    decision_memory: DecisionMemory = Field(..., description="Decision outcomes logs")
    identity_graph: IdentityEvolutionGraph = Field(..., description="Identity transition graph")
    weekly_trajectory: WeeklyLifeTrajectory = Field(..., description="Weekly trajectory progression values")
