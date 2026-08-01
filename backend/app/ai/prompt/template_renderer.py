from typing import Any, Dict
from app.ai.framework.errors import PromptError

class TemplateRenderer:
    """Renders prompt templates with format parameters."""

    def render(self, template: str, context: Dict[str, Any]) -> str:
        """Injects context variables into the template string.
        
        Args:
            template: The raw prompt template string.
            context: Flat variables payload.
            
        Returns:
            str: Compiled prompt.
        """
        try:
            return template.format(**context)
        except KeyError as e:
            raise PromptError(f"Missing required parameter '{str(e)}' in prompt template injection.")
        except Exception as e:
            raise PromptError(f"Failed to render prompt template: {str(e)}")
