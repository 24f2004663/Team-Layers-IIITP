from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class OpportunityReadiness(BaseModel):
    """The computed readiness percentage and missing pre-requisites for specialized opportunities."""
    readiness_percentage: float = Field(..., ge=0.0, le=1.0, description="Readiness percentage score")
    missing_skills: List[str] = Field(default_factory=list, description="Missing skills list")
    preparation_time_hours: float = Field(..., description="Estimated study time required to reach readiness")

class SkillGain(BaseModel):
    """The projected percentage adjustment of a specific skill value."""
    skill_name: str = Field(..., description="Target skill name")
    gain_percentage: float = Field(..., ge=0.0, le=1.0, description="Projected gain increment (rate)")

class CuratedBundleExplanation(BaseModel):
    """Explainability trace justifying why this recommendation bundle fits the user's needs."""
    why_this_resource: str = Field(..., description="Justification statement for main resources")
    why_now: str = Field(..., description="Justification for timing selection")
    how_it_supports_mission: str = Field(..., description="Link to active mission goals")
    which_skill_gap_it_closes: str = Field(..., description="Link to diagnosed gaps")
    expected_learning_outcome: str = Field(..., description="Target outcome description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Curation confidence rating")
    alternative_option: str = Field(..., description="Alternative recommended track detail")

class BundleQualityScore(BaseModel):
    """Combined composition rating assessing relevance, diversity, and coverage."""
    relevance: float = Field(..., ge=0.0, le=1.0, description="Aspirations relevance matching rate")
    diversity: float = Field(..., ge=0.0, le=1.0, description="Resource types diversity penalty score")
    time_efficiency: float = Field(..., ge=0.0, le=1.0, description="Effort duration efficiency rating")
    skill_coverage: float = Field(..., ge=0.0, le=1.0, description="Target gap coverage percentage")
    historical_success: float = Field(..., ge=0.0, le=1.0, description="User past success factor score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall curation confidence rate")

class ExperienceBundle(BaseModel):
    """A compiled bundle of learning materials composed as an experience path for one ExecutionUnit."""
    bundle_id: UUID = Field(default_factory=uuid4, description="Unique bundle ID")
    primary_video: str = Field(..., description="Curated tutorial or lecture video URL")
    official_documentation: str = Field(..., description="Prerequisite reference documentation link")
    practice_exercise: str = Field(..., description="Coding sandbox or practice exercise task")
    mini_project: str = Field(..., description="Hands-on mini project build task")
    github_repository: str = Field(..., description="Reference code repository link")
    quiz: str = Field(..., description="Knowledge verification quiz link")
    optional_reading: str = Field(..., description="Optional reading articles")
    reflection_question: str = Field(..., description="Personal review/reflection prompt")
    estimated_completion_time_minutes: int = Field(..., description="Combined estimated effort duration")
    expected_skill_gains: List[SkillGain] = Field(default_factory=list, description="Skill growth estimates")
    resource_diversity_score: float = Field(..., ge=0.0, le=1.0, description="Diversity penalty score")
    path_order_sequence: List[str] = Field(default_factory=list, description="Optimal chronological path steps")
    standard_option: str = Field(..., description="Baseline standard bundle overview")
    fast_track_option: str = Field(..., description="Condensed fast track option overview")
    deep_dive_option: str = Field(..., description="Expanded deep dive details")
    quality_score: BundleQualityScore = Field(..., description="Composite quality metrics")
    explanation: CuratedBundleExplanation = Field(..., description="Explainability trace details")

class RankedOpportunity(BaseModel):
    """A scored learning opportunity candidate ranked for curating recommendations."""
    resource_name: str = Field(..., description="Name of learning resource")
    resource_type: str = Field(..., description="Type (e.g. Course, Video, Book, Paper, Hackathon)")
    url: str = Field(..., description="Access URL link")
    score: float = Field(..., ge=0.0, le=1.0, description="Computed compatibility score")
    rank: int = Field(..., description="Ordinal placement rank")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Structural quality rating")
    opportunity_readiness: OpportunityReadiness = Field(..., description="Target opportunity readiness metadata")

class CuratorAgentOutput(BaseModel):
    """The rich conformed output model returned by the Curator Agent."""
    bundle: ExperienceBundle = Field(..., description="The curated Experience Bundle")
    candidates_ranked: List[RankedOpportunity] = Field(default_factory=list, description="Ranked list of evaluated opportunity candidates")
