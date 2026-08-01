from typing import Dict
from app.ai.llm.base import BaseLLM
from app.ai.llm.gemini import GeminiLLM

class LLMFactory:
    """Factory creating and caching active BaseLLM adapter implementations."""

    def __init__(self):
        self._cache: Dict[str, BaseLLM] = {}

    def get_llm(self, provider: str = "gemini") -> BaseLLM:
        """Returns cached or new instance of requested LLM provider.
        
        Args:
            provider: Provider name key (e.g. 'gemini').
            
        Returns:
            BaseLLM: Conformed adapter instance.
        """
        p_key = provider.lower()
        if p_key not in self._cache:
            if p_key == "gemini":
                self._cache[p_key] = GeminiLLM()
            else:
                raise ValueError(f"Unrecognized LLM provider key: '{provider}'")
        return self._cache[p_key]

# Instantiated factory singleton
llm_factory = LLMFactory()
