from typing import Any, Dict
from app.engines.causal_reasoning.engine import CausalReasoningEngine

class LearningLoopContextBuilder:
    """Formats evidence, outcomes, and causal reasoning outputs for Learning Loop prompt compilation."""

    def __init__(self):
        self.causal_engine = CausalReasoningEngine()

    def build_prompt_variables(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts raw list dicts into clean string outputs for the prompt template.
        
        Args:
            context_data: Preprocessed parameters.
            
        Returns:
            Dict[str, Any]: Prompt string parameters.
        """
        ev = context_data.get("evidence", {})
        out = context_data.get("outcome", {})
        beh = context_data.get("behavior", {})
        
        # Build causal analysis variables
        causal = self.causal_engine.analyze_causes(
            interruptions_count=ev.get("interruptions_count", 0),
            energy_level=ev.get("energy_level", "High"),
            mood_value=ev.get("mood_value", "Focused")
        )
        
        ev_block = (
            f"- Completed Missions: {ev.get('completed_missions_count')}\n"
            f"- Completed Tasks: {ev.get('completed_execution_units')}\n"
            f"- Focus Time: {ev.get('session_duration_minutes')} minutes\n"
            f"- Interruptions: {ev.get('interruptions_count')}\n"
        )
        
        out_block = (
            f"- Mission Success Rate: {out.get('mission_success_rate')}\n"
            f"- Learning Success Rate: {out.get('learning_success_rate')}\n"
            f"- Skill Gain Ratio: {out.get('skill_gain_ratio')}\n"
        )
        
        causal_block = (
            f"- Root Cause: {causal.root_cause}\n"
            f"- Causal Confidence: {causal.confidence}\n"
            f"- Recommended Intervention: {causal.recommended_intervention}\n"
        )
        
        return {
            "evidence_block": ev_block,
            "outcome_block": out_block,
            "causal_block": causal_block,
            "current_consistency": str(beh.get("consistency_score", 0.60))
        }
