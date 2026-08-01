from typing import List
from pydantic import BaseModel, Field

class DecomposerNode(BaseModel):
    """A node inside the decomposition graphs mapping a specific skill topic or task milestone."""
    id: str = Field(..., description="Unique node identifier")
    name: str = Field(..., description="Descriptive name")
    description: str = Field(..., description="Context explanation")
    dependencies: List[str] = Field(default_factory=list, description="IDs of prerequisite nodes")
    difficulty: str = Field(..., description="Difficulty rating (Easy, Medium, Hard)")
    estimated_hours: float = Field(..., description="Estimated effort duration")

class GoalGraph(BaseModel):
    """The generated roadmap detailing sequential topics (Knowledge) and prerequisites (Dependency)."""
    knowledge_graph: List[DecomposerNode] = Field(default_factory=list, description="Skill structural tree")
    dependency_graph: List[DecomposerNode] = Field(default_factory=list, description="Execution sequence dependencies")
    quarterly_milestones: List[str] = Field(default_factory=list, description="High-level milestones")
    monthly_milestones: List[str] = Field(default_factory=list, description="Monthly milestones")
    weekly_milestones: List[str] = Field(default_factory=list, description="Actionable week goals")

class GoalDecomposer:
    """Decomposes high-level goals into dependency graphs and milestones roadmap."""

    def decompose(self, high_level_goal: str) -> GoalGraph:
        """Decomposes goal and yields dependency-aware roadmaps.
        
        Args:
            high_level_goal: High-level target goal.
            
        Returns:
            GoalGraph: Decoupled graphs and milestones.
        """
        # 1. Build Knowledge Graph (structural hierarchy)
        k_graph = [
            DecomposerNode(
                id="ml-core", name="Machine Learning Core", description="Theoretical foundations",
                dependencies=[], difficulty="Hard", estimated_hours=40.0
            ),
            DecomposerNode(
                id="ml-regression", name="Regression Models", description="Linear and logistic regression algorithms",
                dependencies=["ml-core"], difficulty="Medium", estimated_hours=15.0
            ),
            DecomposerNode(
                id="ml-classification", name="Classification Models", description="SVM, decision trees, random forests",
                dependencies=["ml-core"], difficulty="Medium", estimated_hours=20.0
            )
        ]
        
        # 2. Build Dependency Graph (chronological execution prerequisites)
        d_graph = [
            DecomposerNode(
                id="python-base", name="Python Fundamentals", description="Base syntax and logic structures",
                dependencies=[], difficulty="Easy", estimated_hours=10.0
            ),
            DecomposerNode(
                id="numpy-data", name="NumPy & Arrays", description="Mathematical vector operations",
                dependencies=["python-base"], difficulty="Medium", estimated_hours=12.0
            ),
            DecomposerNode(
                id="pandas-data", name="Pandas DataFrames", description="Tabular data loading and cleaning",
                dependencies=["numpy-data"], difficulty="Medium", estimated_hours=15.0
            ),
            DecomposerNode(
                id="ml-intro", name="ML Foundations", description="Scikit-learn modeling",
                dependencies=["pandas-data"], difficulty="Hard", estimated_hours=30.0
            )
        ]
        
        # 3. Generate Roadmap Milestones
        quarterly = ["Q1: Acquire programming fundamentals", "Q2: Master core modeling algorithms"]
        monthly = ["Month 1: Python bases", "Month 2: NumPy & Pandas manipulation", "Month 3: Basic ML algorithms"]
        weekly = ["Week 1: Logic syntax", "Week 2: Array indexing", "Week 3: DataFrame grouping"]
        
        return GoalGraph(
            knowledge_graph=k_graph,
            dependency_graph=d_graph,
            quarterly_milestones=quarterly,
            monthly_milestones=monthly,
            weekly_milestones=weekly
        )
