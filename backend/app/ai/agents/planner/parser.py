from app.ai.parser.response_mapper import ResponseMapper
from app.ai.agents.planner.schemas import PlannerAgentOutput
from app.ai.framework.messages import AIResponse

class PlannerParser:
    """Parser utilizing ResponseMapper to decode JSON outputs into PlannerAgentOutputs."""

    def __init__(self):
        self.mapper = ResponseMapper()

    def parse_output(self, response: AIResponse) -> PlannerAgentOutput:
        """Parses LLM response content into PlannerAgentOutput.
        
        Args:
            response: Input LLM AIResponse.
            
        Returns:
            PlannerAgentOutput: Conformed planner agent output model.
        """
        return self.mapper.map_response(response.content, PlannerAgentOutput)
