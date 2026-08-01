import json
import re
from typing import Any, Optional
from app.infrastructure.logging.logger import logger

class JSONRepair:
    """Attempts to recover and repair malformed JSON payloads returned by LLMs."""

    def repair_json_string(self, text: str) -> str:
        """Cleans and repairs common JSON syntax errors.
        
        Args:
            text: Raw candidate string.
            
        Returns:
            str: Repaired JSON string.
        """
        cleaned = text.strip()
        
        # 1. Extract JSON block starting from first '{' or '[' if present
        first_brace = cleaned.find("{")
        first_bracket = cleaned.find("[")
        if first_brace != -1 or first_bracket != -1:
            start_idx = first_brace if (first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket)) else first_bracket
            cleaned = cleaned[start_idx:]
            
        # 2. Close open string quotes if odd number of quotes
        # Ignore escaped quotes when counting
        quote_count = len(re.findall(r'(?<!\\)"', cleaned))
        if quote_count % 2 != 0:
            cleaned += '"'
            
        # 3. Basic brackets balancing
        open_brackets = cleaned.count("[")
        close_brackets = cleaned.count("]")
        if open_brackets > close_brackets:
            cleaned += "]" * (open_brackets - close_brackets)

        # 4. Basic braces balancing
        open_braces = cleaned.count("{")
        close_braces = cleaned.count("}")
        if open_braces > close_braces:
            cleaned += "}" * (open_braces - close_braces)
            
        # 4. Trailing commas removal
        cleaned = re.sub(r",\s*(\}|\])", r"\1", cleaned)
        return cleaned

    def try_parse_repaired(self, text: str) -> Optional[Any]:
        """Attempts to parse JSON after applying repairs.
        
        Args:
            text: Candidate JSON text.
            
        Returns:
            Optional[Any]: Parsed JSON or None if irreparable.
        """
        repaired = self.repair_json_string(text)
        try:
            return json.loads(repaired)
        except Exception as e:
            logger.warning("JSONRepair failed to recover malformed JSON", error=str(e))
            return None
