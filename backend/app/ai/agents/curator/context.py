from typing import Any, Dict

class CuratorContextBuilder:
    """Formats normalized learning parameters and candidates for Curator prompt compilation."""

    def build_prompt_variables(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts raw list dicts into clean string outputs for the prompt template.
        
        Args:
            context_data: Preprocessed parameters.
            
        Returns:
            Dict[str, Any]: Prompt string parameters.
        """
        ctx = context_data.get("learning_context", {})
        candidates = context_data.get("candidate_opportunities", [])
        
        ctx_block = (
            f"- Topic: {ctx.get('topic')}\n"
            f"- Goal: {ctx.get('learning_goal')}\n"
            f"- Preferred learning style: {ctx.get('preferred_learning_style')}\n"
            f"- Available Time limit: {ctx.get('available_time')} mins\n"
            f"- Energy Level: {ctx.get('energy_level')}\n"
        )
        
        candidates_block = ""
        for i, c in enumerate(candidates, 1):
            candidates_block += f"{i}. {c['name']} (Type: {c['type']}, URL: {c['url']}, Base Quality: {c['quality']})\n"
            
        return {
            "learning_context_block": ctx_block,
            "candidates_block": candidates_block
        }
