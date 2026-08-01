import os
from typing import Any, Dict
from app.ai.prompt.prompt_builder import PromptBuilder as BasePromptBuilder

class PlannerPromptBuilder:
    """Loads and compiles prompt templates located in the local planner/prompts folder."""

    def __init__(self):
        self.base_builder = BasePromptBuilder()
        self.dir_path = os.path.dirname(os.path.abspath(__file__))

    def get_compiled_prompt(self, state: Any, context: Any, variables: Dict[str, Any], version: str = "v1") -> str:
        """Loads and renders the local template using the core PromptBuilder.
        
        Args:
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            variables: Context variables dictionary.
            version: Target version name (e.g. 'v1').
            
        Returns:
            str: Compiled prompt.
        """
        template_file = os.path.join(self.dir_path, "prompts", f"{version}.md")
        with open(template_file, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        return self.base_builder.build_prompt(template_content, state, context, variables)
