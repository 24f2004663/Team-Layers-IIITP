from typing import Any, Dict

class IdentityContextBuilder:
    """Converts the preprocessed raw values into formatted strings for prompt substitutions."""

    def build_prompt_variables(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats lists and dictionary fields into pretty bullet points for prompt injection.
        
        Args:
            context_data: Gained preprocessed dictionary.
            
        Returns:
            Dict[str, Any]: Formatted strings dict.
        """
        goals_list = context_data.get("goals", [])
        interests_list = context_data.get("interests", [])
        
        return {
            "goals": ", ".join(goals_list) if goals_list else "None specified",
            "interests": ", ".join(interests_list) if interests_list else "None specified",
            "previous_archetype": context_data.get("previous_archetype", "None"),
            "last_change_reason": context_data.get("last_change_reason", "None"),
            "timeline_length": str(context_data.get("timeline_length", 0))
        }
