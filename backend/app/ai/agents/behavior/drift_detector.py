from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.ai.agents.behavior.schemas import BehaviorProfile

class DriftWarning(BaseModel):
    """Signals behavior drift thresholds breached when comparing current vs historical baselines."""

    drift_detected: bool = Field(False, description="Flag indicating if drift was detected")
    metric: str = Field("", description="The metric that drifted (e.g. consistency)")
    variance: float = Field(0.0, description="Rate of deviation from base line")
    description: str = Field("", description="Textual explanation of warning details")

class BehaviorDriftDetector:
    """Compares current BehaviorProfile attributes against previous profiles to check for drift."""

    def detect_drift(self, current: BehaviorProfile, baseline: Optional[Dict[str, Any]]) -> List[DriftWarning]:
        """Runs checks comparing current profile indicators against baselines.
        
        Args:
            current: The newly generated BehaviorProfile.
            baseline: The historical profile data dictionary.
            
        Returns:
            List[DriftWarning]: Detected drift alerts list.
        """
        warnings = []
        if not baseline:
            return warnings
            
        # 1. Check Consistency score drift
        base_consistency = baseline.get("consistency_score", 0.8)
        variance = current.consistency_score - base_consistency
        
        # If consistency drops by 15% or more
        if variance <= -0.15:
            warnings.append(
                DriftWarning(
                    drift_detected=True,
                    metric="consistency_score",
                    variance=round(variance, 3),
                    description=f"Your study consistency has dropped by {int(abs(variance)*100)}% compared with your baseline."
                )
            )
            
        # 2. Check Attention span drift
        base_attention = baseline.get("attention_span_minutes", 30)
        span_variance = current.attention_span_minutes - base_attention
        
        if span_variance <= -10:
            warnings.append(
                DriftWarning(
                    drift_detected=True,
                    metric="attention_span_minutes",
                    variance=float(span_variance),
                    description=f"Your focus attention span has decreased by {int(abs(span_variance))} minutes."
                )
            )
            
        return warnings
