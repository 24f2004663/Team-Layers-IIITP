from app.ai.parser.response_mapper import ResponseMapper
from app.ai.agents.behavior.schemas import BehaviorProfile
from app.ai.framework.messages import AIResponse

class BehaviorParser:
    """Parser utilizing ResponseMapper to decode JSON outputs into BehaviorProfiles."""

    def __init__(self):
        self.mapper = ResponseMapper()

    def parse_profile(self, response: AIResponse) -> BehaviorProfile:
        """Parses LLM response content into BehaviorProfile.
        
        Args:
            response: Input LLM AIResponse.
            
        Returns:
            BehaviorProfile: Conformed behavior profile model.
        """
        return self.mapper.map_response(response.content, BehaviorProfile)
