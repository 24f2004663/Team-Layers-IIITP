from typing import List, Dict, Any
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from app.engines.mission.schemas import Mission, ExecutionUnit, MissionStatus

class MissionGenerator:
    """Generates conformed learning missions and associated granular ExecutionUnits."""

    def generate_missions(
        self,
        decision_priority: str,
        strategy_name: str,
        goal_graph: Any
    ) -> List[Mission]:
        """Maps nodes in dependency graphs to clear learning missions with execution steps.
        
        Args:
            decision_priority: The primary priority metric.
            strategy_name: Selected growth strategy.
            goal_graph: Generated GoalGraph.
            
        Returns:
            List[Mission]: Generated list of candidate missions.
        """
        missions = []
        deadline_str = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        
        # 1. Mission 1: Python Syntax Basics
        m1_id = uuid4()
        m1_units = [
            ExecutionUnit(
                id=uuid4(), mission_id=m1_id, title="Review variables and data structures basics",
                estimated_duration=20, required_energy="Low", required_focus="Medium",
                dependencies=[], completion_criteria=["Understood memory models"], priority=0.9
            ),
            ExecutionUnit(
                id=uuid4(), mission_id=m1_id, title="Practice list comprehensions and dictionaries",
                estimated_duration=40, required_energy="High", required_focus="High",
                dependencies=[], completion_criteria=["Wrote 5 dictionary lookups"], priority=0.8
            )
        ]
        
        missions.append(
            Mission(
                mission_id=m1_id,
                title="Python Syntax Basics",
                objective="Acquire syntax logic structures",
                description="Complete base loops and conditions exercises.",
                supporting_gap=f"Prerequisite gap for {decision_priority}",
                supporting_strategy=strategy_name,
                success_criteria=["Run 5 coding loops", "Define 3 class interfaces"],
                estimated_duration=60,
                difficulty="Easy",
                priority=0.9,
                deadline=deadline_str,
                energy_requirement="Medium",
                focus_requirement="Medium",
                confidence=0.95,
                reasoning="Prerequisite fundamental syntax must be acquired first.",
                status=MissionStatus.CREATED,
                execution_units=m1_units
            )
        )
        
        # 2. Mission 2: NumPy Vectors
        m2_id = uuid4()
        m2_units = [
            ExecutionUnit(
                id=uuid4(), mission_id=m2_id, title="Understand matrix multiplication theories",
                estimated_duration=30, required_energy="Medium", required_focus="High",
                dependencies=[], completion_criteria=["Understood matrix dot product"], priority=0.85
            ),
            ExecutionUnit(
                id=uuid4(), mission_id=m2_id, title="Run numpy exercises locally",
                estimated_duration=60, required_energy="High", required_focus="High",
                dependencies=[], completion_criteria=["Executed dot product locally"], priority=0.75
            )
        ]
        
        missions.append(
            Mission(
                mission_id=m2_id,
                title="NumPy Vectors",
                objective="Learn NumPy vector array mathematics",
                description="Operate linear matrices transformations.",
                supporting_gap=f"Skill Gap for {decision_priority}",
                supporting_strategy=strategy_name,
                success_criteria=["Complete matrix dot product exercises", "Pass numpy assessment"],
                estimated_duration=90,
                difficulty="Medium",
                priority=0.8,
                deadline=deadline_str,
                energy_requirement="High",
                focus_requirement="High",
                confidence=0.90,
                reasoning="Required mathematical operations for modeling dependencies.",
                status=MissionStatus.CREATED,
                execution_units=m2_units
            )
        )
        
        return missions
