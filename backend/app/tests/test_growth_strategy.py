from app.engines.growth_strategy.engine import GrowthStrategyEngine

def test_strategy_engine_plugins():
    engine = GrowthStrategyEngine()
    
    # Test Tiny Habits plugin
    habits = engine.resolve_strategy("Tiny Habits", "Consistency optimization required.")
    assert habits.strategy_name == "Tiny Habits"
    assert "Atomic" in habits.profile.objective or "atomic" in habits.profile.objective or "incremental" in habits.profile.objective
    
    # Test Deep Work plugin
    deep = engine.resolve_strategy("Deep Work", "High focus needed.")
    assert deep.strategy_name == "Deep Work"
    assert len(deep.profile.success_metrics) >= 2
