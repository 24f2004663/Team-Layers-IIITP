from app.ai.parser.response_mapper import ResponseMapper
from app.ai.agents.gap_analysis.schemas import GapAnalysisResult
from app.ai.framework.messages import AIResponse

class GapParser:
    """Parser utilizing ResponseMapper to decode JSON outputs into GapAnalysisResults."""

    def __init__(self):
        self.mapper = ResponseMapper()

    def parse_result(self, response: AIResponse) -> GapAnalysisResult:
        """Parses LLM response content into GapAnalysisResult.
        
        Args:
            response: Input LLM AIResponse.
            
        Returns:
            GapAnalysisResult: Conformed gap analysis model.
        """
        return self.mapper.map_response(response.content, GapAnalysisResult)
