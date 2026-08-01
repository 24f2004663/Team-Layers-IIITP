from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional, Type
from pydantic import BaseModel
from app.ai.framework.messages import AIMessage, AIResponse

class BaseLLM(ABC):
    """Abstract interface defining the requirements for LLM adapters."""

    @abstractmethod
    async def invoke(
        self, 
        messages: List[AIMessage], 
        schema: Optional[Type[BaseModel]] = None,
        system_instruction: Optional[str] = None
    ) -> AIResponse:
        """Invokes the model with conversation history, optionally returning structured output.
        
        Args:
            messages: List of AIMessage items.
            schema: Optional target validation model schema.
            system_instruction: Optional system level context instructions.
            
        Returns:
            AIResponse: Standardized AI response container.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(self, messages: List[AIMessage]) -> AsyncGenerator[str, None]:
        """Streams text chunks response content.
        
        Args:
            messages: List of AIMessage items.
            
        Yields:
            str: Output content chunk.
        """
        raise NotImplementedError

    @abstractmethod
    async def batch(self, inputs: List[List[AIMessage]]) -> List[AIResponse]:
        """Processes multiple conversations concurrently.
        
        Args:
            inputs: Batch of message lists.
            
        Returns:
            List[AIResponse]: Concurrently evaluated responses.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generates semantic float vector embeddings for input text.
        
        Args:
            text: Query string.
            
        Returns:
            List[float]: Mapped float vector.
        """
        raise NotImplementedError

    @abstractmethod
    async def health(self) -> bool:
        """Evaluates health connection parameters.
        
        Returns:
            bool: True if healthy.
        """
        raise NotImplementedError

    @abstractmethod
    async def token_count(self, prompt: str) -> int:
        """Counts tokens for input text.
        
        Args:
            prompt: Text.
            
        Returns:
            int: Token count.
        """
        raise NotImplementedError

    @abstractmethod
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimates execution costs.
        
        Args:
            prompt_tokens: Input tokens.
            completion_tokens: Output tokens.
            
        Returns:
            float: Cost in USD.
        """
        raise NotImplementedError
