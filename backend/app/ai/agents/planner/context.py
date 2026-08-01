from typing import Any, Dict

class PlannerContextBuilder:
    """Formats prioritized missions and calendar limits for the Planner Agent prompt compilation."""

    def build_prompt_variables(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts raw list dicts into clean string outputs for the prompt template.
        
        Args:
            context_data: Preprocessed variables.
            
        Returns:
            Dict[str, Any]: Prompt string parameters.
        """
        missions_list = context_data.get("missions", [])
        beh = context_data.get("behavior_profile", {})
        
        # Build missions block
        missions_block = ""
        for i, m in enumerate(missions_list, 1):
            missions_block += (
                f"{i}. [{m['mission_id']}] {m['title']}\n"
                f"   - Objective: {m['objective']}\n"
                f"   - Duration: {m['estimated_duration']} mins, Priority: {m['priority']}\n"
                f"   - Focus Needed: {m['focus_requirement']}, Energy: {m['energy_requirement']}\n"
            )
        if not missions_block:
            missions_block = "No active missions. Do not schedule anything."
            
        # Build behavior constraints
        beh_block = (
            f"- Focus Style: {beh.get('focus_style', 'Spurt')}\n"
            f"- Average Attention Span: {beh.get('attention_span_minutes', 30)} minutes\n"
            f"- Preferred Session Length: {beh.get('preferred_session_length', 45)} minutes\n"
            f"- Peak Productive Hours: {beh.get('productive_hours', [9, 10, 14, 15])}\n"
            f"- Energy Pattern: {beh.get('energy_pattern', 'Morning Peak')}\n"
        )
        
        return {
            "missions_block": missions_block,
            "behavior_block": beh_block,
            "available_hours": str(context_data.get("available_hours_per_day", 3.0)),
            "today_date": context_data.get("today_date", "Unknown")
        }
