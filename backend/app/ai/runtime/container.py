from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings, Settings
from app.infrastructure.logging.logger import logger
from app.ai.graph.agent_registry import AgentRegistry
from app.ai.runtime.engine import ExecutionEngine
from app.ai.memory.identity.manager import SQLIdentityMemoryManager
from app.ai.memory.behavior.manager import SQLBehaviorMemoryManager
from app.ai.memory.progress.manager import SQLProgressMemoryManager
from app.ai.memory.semantic.manager import MockSemanticMemoryManager
from app.ai.memory.session.manager import MockSessionMemoryManager
from app.knowledge.registry import ProviderRegistry
from app.knowledge.aggregator import KnowledgeAggregator

class DIContainer:
    """Dependency Injection container mapping all core repositories, managers, registries, and engines."""

    def __init__(self):
        self.settings: Settings = settings
        self.logger = logger
        
        # Registries
        self.registry: AgentRegistry = AgentRegistry()
        from app.ai.agents.identity.agent import IdentityAgent
        from app.ai.agents.behavior.agent import BehaviorAgent
        from app.ai.agents.gap_analysis.agent import GapAnalysisAgent
        from app.ai.agents.planner.agent import PlannerAgent
        from app.ai.agents.curator.agent import CuratorAgent
        from app.ai.agents.learning_loop.agent import LearningLoopAgent
        self.registry.register(IdentityAgent())
        self.registry.register(BehaviorAgent())
        self.registry.register(GapAnalysisAgent())
        self.registry.register(PlannerAgent())
        self.registry.register(CuratorAgent())
        self.registry.register(LearningLoopAgent())
        self.provider_registry: ProviderRegistry = ProviderRegistry()
        
        # Engines and Aggregators
        from app.ai.framework.agent_runtime import AgentRuntime
        self.agent_runtime: AgentRuntime = AgentRuntime()
        self.engine: ExecutionEngine = ExecutionEngine(self.registry)
        self.knowledge_aggregator: KnowledgeAggregator = KnowledgeAggregator(self.provider_registry)
        
        # Memory Managers (Mocked or uninitialized, bound to DB dynamically per request)
        self.identity_memory: Optional[SQLIdentityMemoryManager] = None
        self.behavior_memory: Optional[SQLBehaviorMemoryManager] = None
        self.progress_memory: Optional[SQLProgressMemoryManager] = None
        self.semantic_memory: MockSemanticMemoryManager = MockSemanticMemoryManager()
        self.session_memory: MockSessionMemoryManager = MockSessionMemoryManager()

    def bind_database_session(self, db: AsyncSession) -> None:
        """Binds an active SQLAlchemy database session to build the SQL-backed Memory Managers.
        
        Args:
            db: Active database AsyncSession.
        """
        self.identity_memory = SQLIdentityMemoryManager(db)
        self.behavior_memory = SQLBehaviorMemoryManager(db)
        self.progress_memory = SQLProgressMemoryManager(db)
        logger.info("Bound active database session to DIContainer Memory Managers.")

# Singleton container instance
container = DIContainer()
