from typing import Any, Dict

class GapContextBuilder:
    """Formats Identity and Behavior profile properties into readable string templates."""

    def build_prompt_variables(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts raw database payload dicts into formatted prompt blocks.
        
        Args:
            context_data: Raw preprocessed profiles.
            
        Returns:
            Dict[str, Any]: Rendered prompt parameters.
        """
        id_data = context_data.get("identity", {})
        beh_data = context_data.get("behavior", {})
        goals_list = context_data.get("goals", [])
        
        id_block = (
            f"- Identity Summary: {id_data.get('identity_summary', 'None')}\n"
            f"- Career Goal: {id_data.get('career_goal', 'None')}\n"
            f"- Core Values: {', '.join(id_data.get('core_values', []))}\n"
            f"- Strengths: {', '.join(id_data.get('strengths', []))}\n"
        )
        
        beh_block = (
            f"- Focus Style: {beh_data.get('focus_style', 'None')}\n"
            f"- Consistency Score: {beh_data.get('consistency_score', 0.0)}\n"
            f"- Procrastination Level: {beh_data.get('procrastination_level', 'None')}\n"
            f"- Productive Hours: {beh_data.get('productive_hours', [])}\n"
        )
        
        goals_block = "\n".join([f"- {g}" for g in goals_list if g]) if goals_list else "No active goals."
        
        return {
            "identity_profile_block": id_block,
            "behavior_profile_block": beh_block,
            "goals_block": goals_block
        }
