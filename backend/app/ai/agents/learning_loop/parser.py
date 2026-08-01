from app.ai.parser.response_mapper import ResponseMapper
from app.ai.agents.learning_loop.schemas import LearningLoopAgentOutput
from app.ai.framework.messages import AIResponse

class LearningLoopParser:
    """Parser utilizing ResponseMapper to decode JSON outputs into LearningLoopAgentOutputs."""

    def __init__(self):
        self.mapper = ResponseMapper()

    def parse_output(self, response: AIResponse) -> LearningLoopAgentOutput:
        """Parses LLM response content into LearningLoopAgentOutput.
        
        Args:
            response: Input LLM AIResponse.
            
        Returns:
            LearningLoopAgentOutput: Conformed learning loop agent output model.
        """
        return self.mapper.map_response(response.content, LearningLoopAgentOutput)
