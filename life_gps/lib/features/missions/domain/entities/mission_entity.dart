import 'package:flutter/foundation.dart';

@immutable
class MissionEntity {
  final String id;
  final String title;
  final String description;
  final double priority;
  final List<String> targetSkills;

  const MissionEntity({
    required this.id,
    required this.title,
    required this.description,
    required this.priority,
    required this.targetSkills,
  });

  factory MissionEntity.fromJson(Map<String, dynamic> json) => MissionEntity(
        id: json['mission_id']?.toString() ?? '',
        title: json['title'] as String? ?? '',
        description: json['description'] as String? ?? '',
        priority: (json['priority'] as num?)?.toDouble() ?? 0.0,
        targetSkills: List<String>.from(json['target_skills'] ?? []),
      );

  Map<String, dynamic> toJson() => {
        'mission_id': id,
        'title': title,
        'description': description,
        'priority': priority,
        'target_skills': targetSkills,
      };
}
