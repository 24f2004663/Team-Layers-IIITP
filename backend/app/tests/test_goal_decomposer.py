from app.engines.goal_decomposer.engine import GoalDecomposer

def test_goal_decomposition():
    decomposer = GoalDecomposer()
    graph = decomposer.decompose("Become AI Engineer")
    
    # 1. Knowledge Graph assertions
    assert len(graph.knowledge_graph) >= 2
    assert graph.knowledge_graph[0].id == "ml-core"
    
    # 2. Dependency Graph assertions
    assert len(graph.dependency_graph) >= 3
    assert "numpy-data" in graph.dependency_graph[2].dependencies or "python-base" in graph.dependency_graph[1].dependencies
    
    # 3. Roadmap assertions
    assert len(graph.quarterly_milestones) >= 1
    assert len(graph.weekly_milestones) >= 1
