from typing import Any, Type, TypeVar
from pydantic import BaseModel
from app.ai.framework.errors import LLMResponseParsingError

T = TypeVar("T", bound=BaseModel)

class SchemaParser:
    """Validates and instantiates Pydantic schemas from parsed dictionaries."""

    def parse_schema(self, data: Any, schema: Type[T]) -> T:
        """Instantiates a schema from active dictionary data.
        
        Args:
            data: Parsed dictionary or list.
            schema: Target Pydantic model.
            
        Returns:
            T: Instantiated model.
            
        Raises:
            LLMResponseParsingError: If schema validation fails.
        """
        try:
            if isinstance(data, dict):
                return schema(**data)
            else:
                return schema(data)
        except Exception as e:
            raise LLMResponseParsingError(f"Schema validation failed: {str(e)}")
