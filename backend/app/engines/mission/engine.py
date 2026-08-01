from typing import List, Any
from app.engines.mission.schemas import Mission
from app.engines.mission.generator import MissionGenerator
from app.engines.mission.priority import MissionPrioritizer
from app.engines.mission.validator import MissionValidator

class MissionEngine:
    """The central engine managing the lifecycle, sequencing, and metrics prioritization of learning missions."""

    def __init__(self):
        self.generator = MissionGenerator()
        self.prioritizer = MissionPrioritizer()
        self.validator = MissionValidator()

    def generate_and_prioritize(
        self,
        decision_priority: str,
        strategy_name: str,
        goal_graph: Any,
        identity_alignment: float,
        overall_gap_score: float
    ) -> List[Mission]:
        """Generates candidate missions, sorts them by priority weighting, and runs validations.
        
        Args:
            decision_priority: The priority target metric.
            strategy_name: Growth strategy name.
            goal_graph: GoalGraph DAG.
            identity_alignment: Score value.
            overall_gap_score: Score value.
            
        Returns:
            List[Mission]: Sorted, conformed, validated missions list.
        """
        # 1. Generate
        candidates = self.generator.generate_missions(decision_priority, strategy_name, goal_graph)
        
        # 2. Prioritize
        prioritized = self.prioritizer.prioritize_missions(candidates, identity_alignment, overall_gap_score)
        
        # 3. Validate
        self.validator.validate_missions(prioritized)
        
        return prioritized
