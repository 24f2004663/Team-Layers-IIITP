from typing import Dict, List, Optional
from app.ai.agents.base.agent import BaseAgent
from app.ai.graph.workflow import WorkflowStage
from app.infrastructure.logging.logger import logger

class AgentRegistry:
    """Registry managing active Agent instances and resolving them based on capability and stage constraints."""

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Registers an agent into the registry pool.
        
        Args:
            agent: Concrete BaseAgent subclass instance.
        """
        name = agent.metadata.name
        self._agents[name] = agent
        logger.info("Successfully registered agent to registry", agent_name=name, stage=agent.metadata.stage.value)

    def unregister(self, name: str) -> None:
        """Removes a registered agent from the registry.
        
        Args:
            name: Unique name identifier of the agent.
        """
        if name in self._agents:
            del self._agents[name]
            logger.info("Unregistered agent", agent_name=name)

    def resolve(self, stage: WorkflowStage) -> BaseAgent:
        """Resolves the highest priority agent matching the target WorkflowStage.
        
        Args:
            stage: WorkflowStage to satisfy.
            
        Returns:
            BaseAgent: Resolved agent.
            
        Raises:
            ValueError: If no agent matches the stage.
        """
        matched_agents = [
            agent for agent in self._agents.values()
            if agent.metadata.stage == stage
        ]
        
        if not matched_agents:
            raise ValueError(f"No registered agent supports the stage: '{stage.value}'.")
            
        # Select matching agent with highest priority
        matched_agents.sort(key=lambda x: x.metadata.priority, reverse=True)
        return matched_agents[0]

    def list(self) -> List[str]:
        """Lists names of all registered agents.
        
        Returns:
            List[str]: Registered agent names.
        """
        return list(self._agents.keys())

    def validate(self) -> bool:
        """Checks correctness of all registered agent structures.
        
        Returns:
            bool: True if validation succeeds.
        """
        for name, agent in self._agents.items():
            if not isinstance(agent, BaseAgent):
                logger.error("Registry validation failed: Node is not a BaseAgent subclass", agent_name=name)
                return False
        return True

    def capabilities(self) -> List[str]:
        """Collects all unique capabilities supported by registered agents.
        
        Returns:
            List[str]: Capabilities list.
        """
        all_caps = set()
        for agent in self._agents.values():
            all_caps.update(agent.metadata.capabilities)
        return list(all_caps)
