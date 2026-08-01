import 'package:flutter/foundation.dart';

@immutable
class DashboardSummaryEntity {
  final String archetype;
  final String overallStatus;
  final int activeGoalsCount;
  final int completedTasksCount;
  final double compositeGrowthIndex;

  const DashboardSummaryEntity({
    required this.archetype,
    required this.overallStatus,
    required this.activeGoalsCount,
    required this.completedTasksCount,
    required this.compositeGrowthIndex,
  });

  factory DashboardSummaryEntity.fromJson(Map<String, dynamic> json) =>
      DashboardSummaryEntity(
        archetype: json['archetype'] as String? ?? 'Explorer',
        overallStatus: json['overall_status'] as String? ?? '',
        activeGoalsCount: json['active_goals_count'] as int? ?? 0,
        completedTasksCount: json['completed_tasks_count'] as int? ?? 0,
        compositeGrowthIndex:
            (json['composite_growth_index'] as num?)?.toDouble() ?? 0.0,
      );

  Map<String, dynamic> toJson() => {
        'archetype': archetype,
        'overall_status': overallStatus,
        'active_goals_count': activeGoalsCount,
        'completed_tasks_count': completedTasksCount,
        'composite_growth_index': compositeGrowthIndex,
      };
}

@immutable
class DashboardTodayEntity {
  final String? currentMission;
  final List<Map<String, dynamic>> agenda;
  final int totalFocusedMinutes;
  final int breaksCount;

  const DashboardTodayEntity({
    this.currentMission,
    required this.agenda,
    required this.totalFocusedMinutes,
    required this.breaksCount,
  });

  factory DashboardTodayEntity.fromJson(Map<String, dynamic> json) =>
      DashboardTodayEntity(
        currentMission: json['current_mission'] as String?,
        agenda: List<Map<String, dynamic>>.from(
          (json['agenda'] as List? ?? [])
              .map((e) => Map<String, dynamic>.from(e as Map)),
        ),
        totalFocusedMinutes: json['total_focused_minutes'] as int? ?? 0,
        breaksCount: json['breaks_count'] as int? ?? 0,
      );

  Map<String, dynamic> toJson() => {
        'current_mission': currentMission,
        'agenda': agenda,
        'total_focused_minutes': totalFocusedMinutes,
        'breaks_count': breaksCount,
      };
}

@immutable
class DashboardProgressEntity {
  final double completionRate;
  final double habitsAdherence;
  final Map<String, double> energyLevels;
  final double consistencyDelta;

  const DashboardProgressEntity({
    required this.completionRate,
    required this.habitsAdherence,
    required this.energyLevels,
    required this.consistencyDelta,
  });

  factory DashboardProgressEntity.fromJson(Map<String, dynamic> json) =>
      DashboardProgressEntity(
        completionRate: (json['completion_rate'] as num?)?.toDouble() ?? 0.0,
        habitsAdherence: (json['habits_adherence'] as num?)?.toDouble() ?? 0.0,
        energyLevels: Map<String, double>.from(
          (json['energy_levels'] as Map? ?? {})
              .map((k, v) => MapEntry(k.toString(), (v as num).toDouble())),
        ),
        consistencyDelta:
            (json['consistency_delta'] as num?)?.toDouble() ?? 0.0,
      );

  Map<String, dynamic> toJson() => {
        'completion_rate': completionRate,
        'habits_adherence': habitsAdherence,
        'energy_levels': energyLevels,
        'consistency_delta': consistencyDelta,
      };
}

@immutable
class DashboardFutureEntity {
  final double predictedSuccessRate;
  final double calibrationFactor;
  final double growthTrajectoryMatch;
  final List<String> recommendedInterventions;

  const DashboardFutureEntity({
    required this.predictedSuccessRate,
    required this.calibrationFactor,
    required this.growthTrajectoryMatch,
    required this.recommendedInterventions,
  });

  factory DashboardFutureEntity.fromJson(Map<String, dynamic> json) =>
      DashboardFutureEntity(
        predictedSuccessRate:
            (json['predicted_success_rate'] as num?)?.toDouble() ?? 0.0,
        calibrationFactor:
            (json['calibration_factor'] as num?)?.toDouble() ?? 0.0,
        growthTrajectoryMatch:
            (json['growth_trajectory_match'] as num?)?.toDouble() ?? 0.0,
        recommendedInterventions:
            List<String>.from(json['recommended_interventions'] ?? []),
      );

  Map<String, dynamic> toJson() => {
        'predicted_success_rate': predictedSuccessRate,
        'calibration_factor': calibrationFactor,
        'growth_trajectory_match': growthTrajectoryMatch,
        'recommended_interventions': recommendedInterventions,
      };
}

@immutable
class DashboardFullEntity {
  final DashboardSummaryEntity summary;
  final DashboardTodayEntity today;
  final DashboardProgressEntity progress;
  final DashboardFutureEntity future;

  const DashboardFullEntity({
    required this.summary,
    required this.today,
    required this.progress,
    required this.future,
  });

  factory DashboardFullEntity.fromJson(Map<String, dynamic> json) =>
      DashboardFullEntity(
        summary: DashboardSummaryEntity.fromJson(
            json['summary'] as Map<String, dynamic>? ?? {}),
        today: DashboardTodayEntity.fromJson(
            json['today'] as Map<String, dynamic>? ?? {}),
        progress: DashboardProgressEntity.fromJson(
            json['progress'] as Map<String, dynamic>? ?? {}),
        future: DashboardFutureEntity.fromJson(
            json['future'] as Map<String, dynamic>? ?? {}),
      );

  Map<String, dynamic> toJson() => {
        'summary': summary.toJson(),
        'today': today.toJson(),
        'progress': progress.toJson(),
        'future': future.toJson(),
      };
}
