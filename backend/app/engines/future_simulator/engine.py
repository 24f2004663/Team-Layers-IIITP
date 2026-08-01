from typing import List, Dict
from pydantic import BaseModel, Field

class InterventionImpact(BaseModel):
    """The simulated impact details of a specific focus optimization intervention."""
    intervention_name: str = Field(..., description="Name of intervention")
    metric_changes: Dict[str, float] = Field(default_factory=dict, description="Projected metric adjustments (rates)")

class FutureScenario(BaseModel):
    """The projected future state output mapping a specific behavioral scenario path."""
    scenario_name: str = Field(..., description="Scenario description path")
    time_horizon_days: int = Field(..., description=" Horizon delta in days")
    goal_completion_probability: float = Field(..., ge=0.0, le=1.0, description="Likely completion score")
    readiness_scores: Dict[str, float] = Field(default_factory=dict, description="Specific category readiness metrics")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Threat risk rate")
    reasoning: str = Field(..., description="Logic trace explaining the scenario projection findings")

class SimulationResult(BaseModel):
    """The conformed scenarios comparison compilation detailing multiple futures."""
    best_projected_scenario: str = Field(..., description="The scenario name showing optimal outcomes")
    scenarios: List[FutureScenario] = Field(default_factory=list, description="Computed scenarios list")
    interventions: List[InterventionImpact] = Field(default_factory=list, description="Intervention impact mappings")

class FutureSimulator:
    """Simulates outcomes, readiness scores, and expected impacts under multiple scenarios and interventions."""

    def run_simulation(self, current_consistency: float, current_focus: int) -> SimulationResult:
        """Projects future scenarios and readiness matrices.
        
        Args:
            current_consistency: User's consistency rating.
            current_focus: User's attention span.
            
        Returns:
            SimulationResult: Scenarios and interventions comparison.
        """
        # 1. Calculate Readiness scores
        base_readiness = {
            "AI Engineer Readiness": round(min(0.95, current_consistency * 0.8), 2),
            "Backend Readiness": round(min(0.95, current_consistency * 0.9), 2),
            "Interview Readiness": round(min(0.95, current_consistency * 0.4), 2),
            "Portfolio Readiness": round(min(0.95, current_consistency * 0.6), 2)
        }
        
        # 2. Build Multiple Futures Scenarios
        scenarios = [
            FutureScenario(
                scenario_name="Scenario A: Current Path",
                time_horizon_days=90,
                goal_completion_probability=round(current_consistency * 0.7, 2),
                readiness_scores=base_readiness,
                risk_score=round(1.0 - current_consistency, 2),
                reasoning="Current habits suggest average completion rates due to low consistency thresholds."
            ),
            FutureScenario(
                scenario_name="Scenario B: Consistency Boost",
                time_horizon_days=90,
                goal_completion_probability=round(min(1.0, current_consistency * 1.2), 2),
                readiness_scores={k: round(min(1.0, v * 1.15), 2) for k, v in base_readiness.items()},
                risk_score=round(max(0.05, (1.0 - current_consistency) * 0.5), 2),
                reasoning="Boosting consistency completion indicators increases all readiness categories."
            ),
            FutureScenario(
                scenario_name="Scenario C: Weekend Deep Work Focus",
                time_horizon_days=90,
                goal_completion_probability=round(min(1.0, current_consistency * 1.1), 2),
                readiness_scores={k: round(min(1.0, v * 1.1), 2) for k, v in base_readiness.items()},
                risk_score=round(max(0.1, (1.0 - current_consistency) * 0.7), 2),
                reasoning="Focusing on weekend blocks improves core skills acquisition velocity."
            )
        ]
        
        # 3. Simulate Intervention Impacts
        interventions = [
            InterventionImpact(
                intervention_name="+30 min Deep Work",
                metric_changes={"Focus": 0.18, "Consistency": 0.11, "Goal Completion": 0.22}
            ),
            InterventionImpact(
                intervention_name="+2 Atomic Habits daily",
                metric_changes={"Consistency": 0.25, "Focus": 0.05, "Goal Completion": 0.15}
            )
        ]
        
        return SimulationResult(
            best_projected_scenario="Scenario B: Consistency Boost",
            scenarios=scenarios,
            interventions=interventions
        )
