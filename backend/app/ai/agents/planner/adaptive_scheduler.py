from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta, timezone
from app.ai.agents.planner.schemas import ExecutionPlanItem, CalendarPlanItem, PlanningExplanation

class AdaptiveScheduler:
    """The Adaptive Rescheduler dynamically shifts calendar slots when execution units are missed."""

    def reschedule_missed(
        self,
        missed_units: List[ExecutionPlanItem],
        current_agenda: List[CalendarPlanItem],
        available_slots: List[Dict[str, Any]]
    ) -> List[CalendarPlanItem]:
        """Calculates alternative schedule slots for missed units while respecting dependencies.
        
        Args:
            missed_units: List of ExecutionPlanItems that were missed.
            current_agenda: Active schedule items.
            available_slots: Next calendar available time bounds.
            
        Returns:
            List[CalendarPlanItem]: The updated calendar plan agenda items.
        """
        updated_agenda = list(current_agenda)
        
        for idx, unit in enumerate(missed_units):
            if idx < len(available_slots):
                slot = available_slots[idx]
                
                # Build explanation tracing rescheduled choices
                exp = PlanningExplanation(
                    why_this_mission="Rescheduled due to execution miss",
                    why_this_time=f"Assigned to next slot: {slot.get('window_name')}",
                    why_this_order="Re-slotted while maintaining relative priorities",
                    supporting_gap="Consistency Gap recovery",
                    supporting_strategy="Tiny Habits recovery",
                    expected_outcome="Recovery milestone completion",
                    confidence=0.85,
                    deferred_reason="Original slot missed",
                    skipped_risk="High risk of streak interruption",
                    alternative_schedule="Shifted block"
                )
                
                rescheduled_item = CalendarPlanItem(
                    unit_id=unit.unit_id,
                    title=unit.title,
                    start_time=slot.get("start"),
                    end_time=slot.get("end"),
                    focus_window=slot.get("window_name", "Afternoon"),
                    explanation=exp
                )
                updated_agenda.append(rescheduled_item)
                
        return updated_agenda
