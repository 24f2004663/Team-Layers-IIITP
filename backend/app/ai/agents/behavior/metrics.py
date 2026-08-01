import math
from typing import List, Tuple
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.ai.agents.behavior.schemas import BehaviorObservation, BehaviorProfile, GrowthInsight
from app.ai.agents.identity.schemas import IdentityProfile

class AlignmentResult(BaseModel):
    """The evaluated alignment result checking identity mapping compatibility with actual behavior logs."""

    alignment_score: float = Field(..., ge=0.0, le=1.0, description="Overall matching alignment rating")
    strengths: List[str] = Field(default_factory=list, description="Aligned characteristics and positive matches")
    conflicts: List[str] = Field(default_factory=list, description="Conflict points indicating misalignment")
    reasoning: str = Field(..., description="Details and context explaining score calculations")
    examples: List[str] = Field(default_factory=list, description="Specific matching examples")

class ConfidenceDecay:
    """Calculates multi-dimensional confidence weights based on Evidence, Recency, and Frequency."""

    def __init__(self, decay_rate_per_day: float = 0.05):
        self.decay_rate = decay_rate_per_day

    def calculate_decayed_confidence(
        self, 
        base_confidence: float, 
        timestamp: datetime, 
        current_time: datetime,
        frequency: int = 1
    ) -> float:
        """Applies a multi-dimensional decay model.
        
        Confidence = Evidence Weight * Recency Weight * Frequency Weight
        """
        # 1. Evidence Weight (base)
        evidence_weight = base_confidence
        
        # 2. Recency Weight (exponential decay)
        obs_time = timestamp
        if obs_time.tzinfo is None:
            obs_time = obs_time.replace(tzinfo=timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)
            
        delta = current_time - obs_time
        days = max(0.0, delta.total_seconds() / 86400.0)
        recency_weight = math.exp(-self.decay_rate * days)
        
        # 3. Frequency Weight (logarithmic scaling)
        frequency_weight = min(1.2, 0.8 + 0.1 * math.log(frequency + 1))
        
        decayed = evidence_weight * recency_weight * frequency_weight
        return max(0.1, min(1.0, round(decayed, 3)))


class GapAnalyzer:
    """Performs gap analysis between who the user wants to become vs observed actions."""

    def analyze_gaps(self, identity: IdentityProfile, behavior: BehaviorProfile) -> Tuple[AlignmentResult, List[GrowthInsight]]:
        """Compares traits and yields an alignment score and structured GrowthInsights.
        
        Args:
            identity: Core IdentityProfile mapping.
            behavior: Core BehaviorProfile mapping.
            
        Returns:
            Tuple[AlignmentResult, List[GrowthInsight]]: Calculated alignment and growth insights.
        """
        strengths = []
        conflicts = []
        examples = []
        insights = []
        
        # Compare style alignments
        style_match = identity.learning_style.lower() == behavior.learning_style.lower()
        if style_match:
            strengths.append(f"Learning styles align on '{identity.learning_style}'.")
            examples.append(f"Learning style match: {identity.learning_style}")
        else:
            conflicts.append(f"Target learning style '{identity.learning_style}' differs from actual '{behavior.learning_style}' style.")
            
        motivation_match = identity.motivation_level.lower() == behavior.motivation_level.lower()
        if motivation_match:
            strengths.append(f"Motivation levels match at '{identity.motivation_level}' level.")
        else:
            conflicts.append(f"Target motivation is '{identity.motivation_level}' but actual performance suggests '{behavior.motivation_level}'.")
            
        # Scoring logic
        score = 0.5
        score += (behavior.consistency_score - 0.5) * 0.4 # consistency shift
        
        if style_match:
            score += 0.15
        else:
            score -= 0.10
            
        if motivation_match:
            score += 0.15
        else:
            score -= 0.10
            
        final_score = max(0.0, min(1.0, round(score, 2)))
        
        # Generate GrowthInsights
        if behavior.consistency_score >= 0.8:
            insights.append(
                GrowthInsight(
                    title="Excellent Consistency",
                    description="Your streak consistency is excellent. You are executing study sessions reliably.",
                    evidence=f"Consistency score is {behavior.consistency_score}",
                    confidence=0.95,
                    recommended_focus="Increase session length or depth of tasks"
                )
            )
        elif behavior.consistency_score < 0.6:
            insights.append(
                GrowthInsight(
                    title="Consistency Gap Detected",
                    description="There is a gap in study consistency. Daily habits need structure.",
                    evidence=f"Consistency score is {behavior.consistency_score}",
                    confidence=0.90,
                    recommended_focus="Establish Pomodoro focus slots to build streaks"
                )
            )
            
        reasoning = (
            f"User shows a {int(final_score * 100)}% alignment between target identity "
            f"and observed behavior. We found {len(strengths)} strengths and {len(conflicts)} conflicts."
        )
        
        alignment = AlignmentResult(
            alignment_score=final_score,
            strengths=strengths,
            conflicts=conflicts,
            reasoning=reasoning,
            examples=examples
        )
        
        return alignment, insights
