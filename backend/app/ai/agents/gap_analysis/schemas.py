from typing import List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class GapCategory(str, Enum):
    """Categorized gap classifications mapping specific user performance issues."""
    KNOWLEDGE = "Knowledge Gap"
    SKILL = "Skill Gap"
    CONSISTENCY = "Consistency Gap"
    MOTIVATION = "Motivation Gap"
    FOCUS = "Focus Gap"
    EXECUTION = "Execution Gap"
    TIME_MANAGEMENT = "Time Management Gap"
    CONFIDENCE = "Confidence Gap"

class IndividualGap(BaseModel):
    """Represents a specific evaluated performance gap."""

    category: GapCategory = Field(..., description="The gap classification category")
    severity: str = Field(..., description="Severity rating (Low, Medium, High)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Evaluation confidence rating")
    supporting_observations: List[str] = Field(default_factory=list, description="Observations backing this gap")
    affected_goals: List[str] = Field(default_factory=list, description="Goal names impacted by this gap")

class PriorityDependency(BaseModel):
    """A directed edge in the priority graph illustrating metric dependency directions."""
    source: str = Field(..., description="The prerequisite or root metric (e.g. Consistency)")
    target: str = Field(..., description="The dependent target metric (e.g. Learning Velocity)")

class PriorityGraph(BaseModel):
    """DAG mapping the optimal sequential optimization path of focus metrics."""
    nodes: List[str] = Field(default_factory=list, description="List of focus priorities")
    edges: List[PriorityDependency] = Field(default_factory=list, description="Directed dependency connections")

class DecisionTrace(BaseModel):
    """The auditable record detailing the exact logic trace used to derive findings."""

    input_signals: List[str] = Field(default_factory=list, description="Input parameters and profiles checked")
    reasoning_steps: List[str] = Field(default_factory=list, description="Chronological logical execution steps")
    evidence_used: List[str] = Field(default_factory=list, description="Key files/observation references cited")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Evaluated tracing confidence")
    tradeoffs: List[str] = Field(default_factory=list, description="Considered alternatives or compromises")

class GapAnalysisResult(BaseModel):
    """The conformed diagnosis mapping identity aspirations against actual behaviors."""

    overall_gap_score: float = Field(..., ge=0.0, le=1.0, description="Computed divergence rating (0.0=Perfect, 1.0=Misaligned)")
    priority_gaps: List[IndividualGap] = Field(default_factory=list, description="Ranked critical gaps")
    behavior_conflicts: List[str] = Field(default_factory=list, description="Identified conflicts between values vs habits")
    identity_alignment: float = Field(..., ge=0.0, le=1.0, description="Overall matching compatibility rating")
    critical_risks: List[str] = Field(default_factory=list, description="Impediments threatening milestone achievements")
    growth_strengths: List[str] = Field(default_factory=list, description="Observed strengths to leverage")
    recommended_strategy: str = Field(..., description="Matching strategy recommendation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall score confidence")
    reasoning: str = Field(..., description="Reasoning statement justifying the gaps analysis findings")
    decision_trace: DecisionTrace = Field(..., description="Explainability trace logs")

class DecisionEngineResult(BaseModel):
    """Resolves what optimization pivots we should prioritize first."""
    primary_priority: str = Field(..., description="The main metric we should focus on optimizing first")
    priority_graph: PriorityGraph = Field(..., description="The Priority Graph indicating metric dependencies")
    reasoning: str = Field(..., description="Logic trace explaining priority choice")
    decision_trace: DecisionTrace = Field(..., description="Explainability trace logs")
