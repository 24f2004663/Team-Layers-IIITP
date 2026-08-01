from typing import List
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from app.ai.agents.behavior.schemas import BehaviorObservation, BehaviorEvidence

class BehaviorEvidenceEngine:
    """Synthesizes raw observations into hypothesis blocks (BehaviorEvidence)."""

    def generate_evidence(self, observations: List[BehaviorObservation]) -> List[BehaviorEvidence]:
        """Groups observations list to build behavioral evidence blocks.
        
        Args:
            observations: List of current observations.
            
        Returns:
            List[BehaviorEvidence]: Evaluated evidence hypotheses.
        """
        evidence_list = []
        now = datetime.now(timezone.utc)
        expiration = now + timedelta(days=14)
        
        # 1. Gather Night Learner Evidence
        night_obs = [obs for obs in observations if obs.timestamp.hour >= 20 or obs.context.get("time_of_day") == "night"]
        if night_obs:
            support_score = min(1.0, len(night_obs) / 3.0)
            evidence_list.append(
                BehaviorEvidence(
                    id=uuid4(),
                    observation_ids=[obs.id for obs in night_obs],
                    hypothesis="Night Learner Hypothesis",
                    support_score=support_score,
                    confidence=round(0.7 + 0.3 * support_score, 2),
                    expires_at=expiration,
                    created_at=now
                )
            )
            
        # 2. Gather Procrastination Evidence
        skipped_obs = [obs for obs in observations if obs.context.get("procrastination_signal") is True or "skipped" in obs.description.lower()]
        if skipped_obs:
            support_score = min(1.0, len(skipped_obs) / 2.0)
            evidence_list.append(
                BehaviorEvidence(
                    id=uuid4(),
                    observation_ids=[obs.id for obs in skipped_obs],
                    hypothesis="Procrastinator Hypothesis",
                    support_score=support_score,
                    confidence=round(0.6 + 0.4 * support_score, 2),
                    expires_at=expiration,
                    created_at=now
                )
            )
            
        # 3. Deep Focus Evidence
        focus_obs = [obs for obs in observations if obs.duration >= 30 and "completed" in obs.description.lower()]
        if focus_obs:
            support_score = min(1.0, len(focus_obs) / 4.0)
            evidence_list.append(
                BehaviorEvidence(
                    id=uuid4(),
                    observation_ids=[obs.id for obs in focus_obs],
                    hypothesis="Deep Focus Hypothesis",
                    support_score=support_score,
                    confidence=round(0.8 + 0.2 * support_score, 2),
                    expires_at=expiration,
                    created_at=now
                )
            )
            
        return evidence_list
