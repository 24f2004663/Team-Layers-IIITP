from app.engines.future_simulator.engine import FutureSimulator

def test_future_simulations():
    simulator = FutureSimulator()
    result = simulator.run_simulation(current_consistency=0.60, current_focus=40)
    
    assert result.best_projected_scenario == "Scenario B: Consistency Boost"
    assert len(result.scenarios) == 3
    
    # Verify readiness scores mapping
    readiness = result.scenarios[0].readiness_scores
    assert "AI Engineer Readiness" in readiness
    assert readiness["AI Engineer Readiness"] == 0.48 # 0.60 * 0.8
    
    # Verify intervention impact
    assert len(result.interventions) >= 1
    assert result.interventions[0].intervention_name == "+30 min Deep Work"
