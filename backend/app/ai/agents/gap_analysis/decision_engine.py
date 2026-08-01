from app.ai.agents.gap_analysis.schemas import (
    GapAnalysisResult, DecisionEngineResult, PriorityGraph, PriorityDependency, DecisionTrace, GapCategory
)

class DecisionEngine:
    """The Decision Engine determines what we should optimize first and builds the Priority Graph."""

    def resolve_priorities(self, gap_result: GapAnalysisResult) -> DecisionEngineResult:
        """Evaluates priority gap listings and maps sequential dependency graphs.
        
        Args:
            gap_result: Output from Gap Analysis.
            
        Returns:
            DecisionEngineResult: Focus prioritization and dependencies.
        """
        # Default priority
        primary = "Consistency"
        
        # Look for consistency gaps
        has_consistency_gap = any(g.category == GapCategory.CONSISTENCY for g in gap_result.priority_gaps)
        
        # Build Priority Graph nodes and edges
        if has_consistency_gap:
            primary = "Consistency"
            nodes = ["Consistency", "Learning Velocity", "Skill Acquisition", "Career Readiness"]
            edges = [
                PriorityDependency(source="Consistency", target="Learning Velocity"),
                PriorityDependency(source="Learning Velocity", target="Skill Acquisition"),
                PriorityDependency(source="Skill Acquisition", target="Career Readiness")
            ]
            reason = "Improving consistency increases every downstream metric. We prioritize Consistency first."
        else:
            primary = "Skill Acquisition"
            nodes = ["Skill Acquisition", "Focus Depth", "Learning Velocity", "Career Readiness"]
            edges = [
                PriorityDependency(source="Skill Acquisition", target="Focus Depth"),
                PriorityDependency(source="Focus Depth", target="Learning Velocity"),
                PriorityDependency(source="Learning Velocity", target="Career Readiness")
            ]
            reason = "Consistency is stable. We prioritize Skill Acquisition depth next."
            
        trace = DecisionTrace(
            input_signals=["GapAnalysisResult.priority_gaps"],
            reasoning_steps=[
                f"Checked for Consistency Gap severity. Found: {has_consistency_gap}",
                "Determined root dependency metric."
            ],
            evidence_used=[f"has_consistency_gap={has_consistency_gap}"],
            confidence=0.95,
            tradeoffs=["Postponed general career readiness tasks to stabilize focus streaks"]
        )
        
        return DecisionEngineResult(
            primary_priority=primary,
            priority_graph=PriorityGraph(nodes=nodes, edges=edges),
            reasoning=reason,
            decision_trace=trace
        )
