class PlatformError(Exception):
    """Base exception for all AI Platform layer failures."""

class LLMError(PlatformError):
    """Exception raised during LLM invocations."""

class LLMResponseParsingError(LLMError):
    """Exception raised when LLM returns invalid structures or failed parses."""

class PromptError(PlatformError):
    """Exception raised during prompt rendering, resolution, or fallback operations."""

class ValidationError(PlatformError):
    """Exception raised when LLM outputs fail structural or business constraint validation."""

class MemoryError(PlatformError):
    """Exception raised during memory operations, rollbacks, or state updates."""

class PipelineError(PlatformError):
    """Exception raised when the AgentRuntime pipeline fails."""

class AgentExecutionError(PlatformError):
    """Exception raised during agent initialization, validation, or execution stages."""
