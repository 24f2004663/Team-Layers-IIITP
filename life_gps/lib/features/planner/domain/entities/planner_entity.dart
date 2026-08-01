import 'package:flutter/foundation.dart';

@immutable
class PlannerEntity {
  final Map<String, dynamic> executionPlan;
  final Map<String, dynamic> calendarPlan;
  final List<String> weeklyObjectives;

  const PlannerEntity({
    required this.executionPlan,
    required this.calendarPlan,
    required this.weeklyObjectives,
  });

  factory PlannerEntity.fromJson(Map<String, dynamic> json) => PlannerEntity(
        executionPlan: Map<String, dynamic>.from(json['execution_plan'] ?? {}),
        calendarPlan: Map<String, dynamic>.from(json['calendar_plan'] ?? {}),
        weeklyObjectives: List<String>.from(json['weekly_objectives'] ?? []),
      );

  Map<String, dynamic> toJson() => {
        'execution_plan': executionPlan,
        'calendar_plan': calendarPlan,
        'weekly_objectives': weeklyObjectives,
      };
}
