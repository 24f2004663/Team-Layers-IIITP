from typing import List
from pydantic import BaseModel, Field

class StrategyProfile(BaseModel):
    """The detailed execution cadence and adaptation parameters for a strategy."""
    objective: str = Field(..., description="Target objective of the strategy")
    reasoning: str = Field(..., description="Explanation of why this strategy was chosen")
    success_metrics: List[str] = Field(default_factory=list, description="Performance indicator targets")
    weekly_cadence: List[str] = Field(default_factory=list, description="Cadence milestones")
    adaptation_rules: List[str] = Field(default_factory=list, description="Rules to dynamically pivot")

class GrowthStrategyOutput(BaseModel):
    """The matched strategy payload returned from the Growth Strategy Engine."""
    strategy_name: str = Field(..., description="Name of strategy plugin selected")
    profile: StrategyProfile = Field(..., description="Calculated profile properties")
