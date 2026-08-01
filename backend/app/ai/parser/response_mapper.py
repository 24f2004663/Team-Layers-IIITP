from typing import Any, Optional, Type, TypeVar
from pydantic import BaseModel
from app.ai.parser.json_parser import JSONParser
from app.ai.parser.repair import JSONRepair
from app.ai.parser.schema_parser import SchemaParser
from app.ai.framework.errors import LLMResponseParsingError

T = TypeVar("T", bound=BaseModel)

class ResponseMapper:
    """Orchestrator decoding raw text response content into conformed schemas with fallback JSON repair."""

    def __init__(self):
        self.parser = JSONParser()
        self.repair = JSONRepair()
        self.schema_parser = SchemaParser()

    def map_response(self, text: str, schema: Type[T]) -> T:
        """Parses and maps input text to schema model.
        
        Args:
            text: Raw input content.
            schema: Target Pydantic model.
            
        Returns:
            T: Conformed model instance.
        """
        # Try standard parse
        try:
            parsed_data = self.parser.parse(text)
        except LLMResponseParsingError as e:
            # Try repair fallbacks
            repaired_data = self.repair.try_parse_repaired(text)
            if repaired_data is not None:
                parsed_data = repaired_data
            else:
                raise e
                
        # Validate schema structure
        return self.schema_parser.parse_schema(parsed_data, schema)
