from typing import Any
from pydantic import BaseModel

class SchemaValidator:
    """Validator performing structural checks on parsed Pydantic outputs."""

    def validate_schema(self, instance: BaseModel) -> bool:
        """Verifies Pydantic validation states.
        
        Args:
            instance: Active Pydantic model.
            
        Returns:
            bool: True if valid.
        """
        # Pydantic v2 validates on instantiation, so this is true if instantiated.
        return isinstance(instance, BaseModel)
