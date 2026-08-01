from typing import List
from app.engines.mission.schemas import Mission

class MissionPrioritizer:
    """Calculates priority scores for candidate missions based on gap and strategy metrics."""

    def prioritize_missions(
        self,
        missions: List[Mission],
        identity_alignment: float,
        overall_gap_score: float
    ) -> List[Mission]:
        """Scores and sorts candidate missions list.
        
        Args:
            missions: Candidate candidate list.
            identity_alignment: Score from gap analysis.
            overall_gap_score: Score from gap analysis.
            
        Returns:
            List[Mission]: Prioritized and sorted list.
        """
        for mission in missions:
            # Score calculation
            base_score = mission.priority
            
            # Boost score based on how critical the gap and how aligned identity targets are
            alignment_factor = identity_alignment * 0.2
            gap_factor = overall_gap_score * 0.2
            
            # Simple priority adjustment
            final_priority = min(1.0, max(0.0, base_score + alignment_factor + gap_factor))
            mission.priority = round(final_priority, 3)
            
        # Sort descending
        missions.sort(key=lambda m: m.priority, reverse=True)
        return missions
