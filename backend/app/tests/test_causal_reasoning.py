from app.engines.causal_reasoning.engine import CausalReasoningEngine

def test_causal_analysis():
    engine = CausalReasoningEngine()
    analysis = engine.analyze_causes(interruptions_count=3, energy_level="Low", mood_value="Tired")
    
    assert "screen" in analysis.root_cause or "sleep" in analysis.root_cause
    assert analysis.confidence == 0.85
    assert len(analysis.evidence) == 2
    
    graph = engine.build_cause_graph()
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 3
