from typing import List, Optional
from pydantic import BaseModel, Field
from app.knowledge.models import OpportunityType

class KnowledgeQuery(BaseModel):
    """The context parameters encapsulating a search inquiry issued by the Planner."""

    goal: str = Field(..., description="Target learning objective or core milestone goal text")
    skills: List[str] = Field(default_factory=list, description="Target list of skills to cultivate")
    learning_style: Optional[str] = Field(None, description="Preferred style (e.g. hands-on, visual)")
    difficulty: Optional[str] = Field(None, description="Target difficulty constraints (e.g. beginner)")
    time_available: Optional[float] = Field(None, description="Maximum available study duration in hours")
    preferred_types: List[OpportunityType] = Field(
        default_factory=list, 
        description="Favorable opportunity formats (e.g. COURSE, VIDEO)"
    )
    language: str = Field("en", description="Preferred language code")
    budget: Optional[float] = Field(None, description="Maximum cost threshold limit")
    excluded_sources: List[str] = Field(default_factory=list, description="Sources/providers to ignore")
    completed_resources: List[str] = Field(default_factory=list, description="URLs or IDs of completed resources to filter out")
