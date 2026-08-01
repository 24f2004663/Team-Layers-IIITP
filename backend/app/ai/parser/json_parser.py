import json
from typing import Any, Dict
from app.ai.framework.errors import LLMResponseParsingError

class JSONParser:
    """Decodes raw string contents into dictionary json models."""

    def parse(self, text: str) -> Any:
        """Parses the input string as JSON.
        
        Args:
            text: Raw string.
            
        Returns:
            Any: Decoded JSON.
            
        Raises:
            LLMResponseParsingError: If decode fails.
        """
        try:
            # Clean up potential markdown formatting wrapping (like ```json ... ```)
            cleaned = text.strip()
            if cleaned.startswith("```"):
                # Remove starting markdown fence
                lines = cleaned.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                cleaned = "\n".join(lines).strip()
                
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise LLMResponseParsingError(f"Failed to parse text as valid JSON: {str(e)}")
