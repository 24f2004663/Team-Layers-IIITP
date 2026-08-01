import 'package:flutter/foundation.dart';

@immutable
class GapAnalysisEntity {
  final String gapDescription;
  final double priorityScore;
  final List<String> targetSkills;
  final String urgency;
  final String recommendsStrategy;

  const GapAnalysisEntity({
    required this.gapDescription,
    required this.priorityScore,
    required this.targetSkills,
    required this.urgency,
    required this.recommendsStrategy,
  });

  factory GapAnalysisEntity.fromJson(Map<String, dynamic> json) =>
      GapAnalysisEntity(
        gapDescription: json['gap_description'] as String? ?? '',
        priorityScore: (json['priority_score'] as num?)?.toDouble() ?? 0.0,
        targetSkills: List<String>.from(json['target_skills'] ?? []),
        urgency: json['urgency'] as String? ?? 'Medium',
        recommendsStrategy: json['recommends_strategy'] as String? ?? '',
      );

  Map<String, dynamic> toJson() => {
        'gap_description': gapDescription,
        'priority_score': priorityScore,
        'target_skills': targetSkills,
        'urgency': urgency,
        'recommends_strategy': recommendsStrategy,
      };
}
