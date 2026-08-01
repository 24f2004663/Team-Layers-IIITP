class LLMError(Exception):
    """Base exception for all LLM adapter failures."""

class LLMConnectionError(LLMError):
    """Exception raised when connection to LLM API fails."""

class LLMRateLimitError(LLMError):
    """Exception raised when API rate limits are hit."""

class LLMResponseParsingError(LLMError):
    """Exception raised when LLM returns invalid structures or failed parses."""

class LLMAuthenticationError(LLMError):
    """Exception raised when API keys or credentials fail validation."""
