from app.ai.parser.response_mapper import ResponseMapper
from app.ai.agents.curator.schemas import CuratorAgentOutput
from app.ai.framework.messages import AIResponse

class CuratorParser:
    """Parser utilizing ResponseMapper to decode JSON outputs into CuratorAgentOutputs."""

    def __init__(self):
        self.mapper = ResponseMapper()

    def parse_output(self, response: AIResponse) -> CuratorAgentOutput:
        """Parses LLM response content into CuratorAgentOutput.
        
        Args:
            response: Input LLM AIResponse.
            
        Returns:
            CuratorAgentOutput: Conformed curator agent output model.
        """
        return self.mapper.map_response(response.content, CuratorAgentOutput)
