import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.ai.agents.base.agent import BaseAgent
from app.ai.graph.state import LifeGPSState
from app.ai.graph.contracts import AgentResult
from app.ai.runtime.context import ExecutionContext
from app.ai.framework.messages import AIMessage, AIResponse
from app.ai.llm.factory import llm_factory
from app.ai.prompt.prompt_builder import PromptBuilder
from app.ai.parser.response_mapper import ResponseMapper
from app.ai.framework.errors import AgentExecutionError, ValidationError
from app.infrastructure.logging.logger import logger

class Explanation(BaseModel):
    """Explainability model providing transparent justifications for agent decisions."""
    reason: str = Field(..., description="The rationale explaining the agent's decision")
    confidence: float = Field(..., description="The confidence level in the decision")
    affected_memory: List[str] = Field(default_factory=list, description="List of memory layers affected")
    decision_trace: List[str] = Field(default_factory=list, description="Step-by-step logs representing the path to the decision")
    sources_used: List[str] = Field(default_factory=list, description="Source context information references used")

class AgentRuntime:
    """The core platform runner executing the full lifecycle of hooks for any BaseAgent."""

    def __init__(self):
        self.prompt_builder = PromptBuilder()
        self.response_mapper = ResponseMapper()

    async def run(self, agent: BaseAgent, state: LifeGPSState, context: ExecutionContext) -> AgentResult:
        """Runs the complete agent hook execution lifecycle.
        
        Args:
            agent: The BaseAgent instance to run.
            state: Active LifeGPSState.
            context: Active ExecutionContext.
            
        Returns:
            AgentResult: Conformed execution outcome.
        """
        start_time = time.time()
        logger.info("AgentRuntime starting run sequence", agent_name=agent.metadata.name)
        
        try:
            # 1. before_execute hook
            await agent.before_execute(state, context)
            
            # 2. preprocess hook
            variables = await agent.preprocess(state, context)
            
            # 3. Resolve and Build prompt
            from app.ai.runtime.container import container
            # Fallback to seed prompt if registry not setup or in test environments
            try:
                versioned_prompt = container.registry.get_prompt(agent.metadata.name.lower().replace("agent", ""))
                template = versioned_prompt.template
            except Exception:
                template = "Process context event: {event} stage: {stage}"
                
            prompt_content = self.prompt_builder.build_prompt(template, state, context, variables)
            
            # 4. before_llm hook
            await agent.before_llm(prompt_content, state, context)
            
            # 5. Invoke LLM Layer
            llm = llm_factory.get_llm(agent.metadata.recommended_model.split("-")[0]) # 'gemini'
            message = AIMessage(role="user", content=prompt_content)
            
            response = await llm.invoke(
                messages=[message],
                system_instruction=agent.metadata.description
            )
            
            # 6. after_llm hook
            await agent.after_llm(response, state, context)
            
            # 7. parse hook
            parsed_output = await agent.parse(response, context)
            
            # 8. validate hook
            if not await agent.validate_output(parsed_output, context):
                raise ValidationError("Output failed validation constraints check.")
                
            # 9. update_memory hook
            await agent.update_memory(parsed_output, state, context)
            
            # 10. postprocess hook
            # Default fallback if agent has not customized postprocess logic
            try:
                result = await agent.postprocess(parsed_output, state, context)
            except NotImplementedError:
                elapsed = time.time() - start_time
                explanation = Explanation(
                    reason=f"{agent.metadata.name} completed successfully.",
                    confidence=0.90,
                    affected_memory=agent.metadata.required_memory,
                    decision_trace=context.trace,
                    sources_used=[context.event.value]
                )
                result = AgentResult(
                    success=True,
                    agent_name=agent.metadata.name,
                    summary=f"Execution completed for agent {agent.metadata.name}.",
                    updated_fields=[],
                    execution_time=elapsed,
                    confidence=0.90,
                    explanation=explanation.model_dump()
                )
                
            # 11. after_execute hook
            await agent.after_execute(state, context, result)
            
            logger.info("AgentRuntime execution completed successfully", agent_name=agent.metadata.name)
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error("AgentRuntime sequence failed", agent_name=agent.metadata.name, error=str(e))
            return AgentResult(
                success=False,
                agent_name=agent.metadata.name,
                summary=f"Agent sequence failed: {str(e)}",
                updated_fields=[],
                errors=[str(e)],
                execution_time=elapsed,
                confidence=0.0
            )
