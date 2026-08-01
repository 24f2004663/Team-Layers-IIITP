from typing import Any, Dict

class BehaviorContextBuilder:
    """Formats raw behavioral observations, evidence, and patterns into string templates."""

    def build_prompt_variables(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts raw list dicts into clean string outputs for the prompt template.
        
        Args:
            context_data: Preprocessed dictionary values.
            
        Returns:
            Dict[str, Any]: Prompt string parameters.
        """
        obs_list = context_data.get("raw_observations", [])
        ev_list = context_data.get("raw_evidence", [])
        pat_list = context_data.get("raw_patterns", [])
        
        # Build observations text list
        obs_text = ""
        for obs in obs_list:
            obs_text += f"- [{obs['timestamp']}] {obs['description']} (Event: {obs['event_type']})\n"
        if not obs_text:
            obs_text = "No observations recorded yet."
            
        # Build evidence text list
        ev_text = ""
        for ev in ev_list:
            ev_text += f"- Hypothesis: {ev['hypothesis']} (Support Score: {ev['support_score']}, Confidence: {ev['confidence']})\n"
        if not ev_text:
            ev_text = "No evidence gathered yet."
            
        # Build patterns text list
        pat_text = ""
        for pat in pat_list:
            pat_text += f"- {pat['pattern_name']} (Frequency: {pat['frequency']}, Confidence: {pat['confidence']}, Trend: {pat['trend']})\n"
        if not pat_text:
            pat_text = "No patterns identified yet."
            
        return {
            "observations_block": obs_text,
            "evidence_block": ev_text,
            "patterns_block": pat_text,
            "observations_count": str(context_data.get("observations_count", 0)),
            "evidence_count": str(context_data.get("evidence_count", 0)),
            "patterns_count": str(context_data.get("patterns_count", 0)),
            "last_active": context_data.get("last_active", "Unknown")
        }
