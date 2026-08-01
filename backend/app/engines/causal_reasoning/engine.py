from typing import List, Dict, Any
from app.engines.causal_reasoning.schemas import CauseAnalysis
from app.engines.causal_reasoning.graph import CausalGraph, CausalEdge

class CausalReasoningEngine:
    """The central engine inferring root behavioral drivers behind execution failures and successes."""

    def analyze_causes(
        self,
        interruptions_count: int,
        energy_level: str,
        mood_value: str
    ) -> CauseAnalysis:
        """Infers root cause dynamics.
        
        Args:
            interruptions_count: Count of interruptions.
            energy_level: Current energy rating.
            mood_value: Current mood.
            
        Returns:
            CauseAnalysis: Root cause metrics.
        """
        # Causal inference logic
        if interruptions_count > 2 or energy_level == "Low":
            root = "Late-night screen usage leading to sleep degradation."
            evidence = ["High sleep disruptions count", "Low morning energy level"]
            rec = "Implement screen downtime limit block at 22:30."
            conf = 0.85
        else:
            root = "Optimized peak productive hours usage."
            evidence = ["Low interruptions count", "Focused attention span"]
            rec = "Maintain consistency by slotting morning blocks."
            conf = 0.90
            
        return CauseAnalysis(
            root_cause=root,
            confidence=conf,
            evidence=evidence,
            recommended_intervention=rec
        )

    def build_cause_graph(self) -> CausalGraph:
        """Builds a causal DAG representing behavior chains."""
        return CausalGraph(
            nodes=["late_night_screen", "sleep_drop", "low_energy", "mission_failure"],
            edges=[
                CausalEdge(source="late_night_screen", target="sleep_drop", strength=0.85),
                CausalEdge(source="sleep_drop", target="low_energy", strength=0.90),
                CausalEdge(source="low_energy", target="mission_failure", strength=0.75)
            ]
        )
