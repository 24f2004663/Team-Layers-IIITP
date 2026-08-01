from typing import Any, Dict
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.prompt.context_builder import ContextBuilder
from app.ai.prompt.template_renderer import TemplateRenderer

class PromptBuilder:
    """Orchestrates prompt compilation by merging context parameters and rendering template targets."""

    def __init__(self):
        self.context_builder = ContextBuilder()
        self.renderer = TemplateRenderer()

    def build_prompt(
        self, 
        template: str, 
        state: LifeGPSState, 
        context: ExecutionContext, 
        variables: Dict[str, Any]
    ) -> str:
        """Runs the context builders and renders the template string.
        
        Args:
            template: Raw prompt template text.
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            variables: Custom dictionary variables.
            
        Returns:
            str: Compiled prompt template.
        """
        full_context = self.context_builder.build_context(state, context, variables)
        return self.renderer.render(template, full_context)
