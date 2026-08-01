from abc import ABC, abstractmethod
from pydantic import BaseModel

class BusinessValidator(ABC):
    """Abstract interface for domain constraints checks on agent outputs."""

    @abstractmethod
    def validate_rules(self, instance: BaseModel) -> bool:
        """Verifies if model attributes fit business rules constraints.
        
        Args:
            instance: Active Pydantic model.
            
        Returns:
            bool: True if passes, False otherwise.
        """
        raise NotImplementedError
