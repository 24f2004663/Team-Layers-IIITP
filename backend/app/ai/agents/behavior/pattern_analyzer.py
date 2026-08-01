from typing import List
from app.ai.agents.behavior.schemas import BehaviorEvidence, BehaviorPattern, PatternStability

class PatternAnalyzer:
    """Analyzes a series of BehaviorEvidence hypotheses to discover patterns with stability indicators."""

    def analyze_patterns(self, evidences: List[BehaviorEvidence]) -> List[BehaviorPattern]:
        """Scans evidence list for hypotheses and maps them to conformed PatternStability metrics.
        
        Args:
            evidences: Synthesized evidence blocks.
            
        Returns:
            List[BehaviorPattern]: Derived patterns with trends.
        """
        patterns = []
        
        for ev in evidences:
            trend = PatternStability.NEW
            if ev.confidence >= 0.90:
                trend = PatternStability.STABLE
            elif ev.confidence >= 0.75:
                trend = PatternStability.EMERGING
                
            if "night" in ev.hypothesis.lower():
                patterns.append(
                    BehaviorPattern(
                        pattern_name="Night Learner",
                        supporting_observations=[f"Evidence ID: {ev.id}"],
                        frequency=len(ev.observation_ids),
                        confidence=ev.confidence,
                        trend=trend
                    )
                )
            elif "procrastinator" in ev.hypothesis.lower():
                patterns.append(
                    BehaviorPattern(
                        pattern_name="Procrastination Tendency",
                        supporting_observations=[f"Evidence ID: {ev.id}"],
                        frequency=len(ev.observation_ids),
                        confidence=ev.confidence,
                        trend=trend
                    )
                )
            elif "focus" in ev.hypothesis.lower():
                patterns.append(
                    BehaviorPattern(
                        pattern_name="Deep Focus Sessions",
                        supporting_observations=[f"Evidence ID: {ev.id}"],
                        frequency=len(ev.observation_ids),
                        confidence=ev.confidence,
                        trend=trend
                    )
                )
                
        return patterns
