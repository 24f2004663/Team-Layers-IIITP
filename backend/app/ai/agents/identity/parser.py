from app.ai.parser.response_mapper import ResponseMapper
from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.framework.messages import AIResponse

class IdentityParser:
    """Parser utilizing the core platform ResponseMapper to validate and decode raw outputs into IdentityProfiles."""

    def __init__(self):
        self.mapper = ResponseMapper()

    def parse_profile(self, response: AIResponse) -> IdentityProfile:
        """Parses the AIResponse content.
        
        Args:
            response: Input LLM AIResponse.
            
        Returns:
            IdentityProfile: Output conformed Pydantic profile.
        """
        return self.mapper.map_response(response.content, IdentityProfile)
