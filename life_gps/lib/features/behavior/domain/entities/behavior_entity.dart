import 'package:flutter/foundation.dart';

@immutable
class BehaviorEntity {
  final String id;
  final String userId;
  final Map<String, dynamic> habits;
  final List<String> cognitivePatterns;
  final Map<String, double> energyLevels;

  const BehaviorEntity({
    required this.id,
    required this.userId,
    required this.habits,
    required this.cognitivePatterns,
    required this.energyLevels,
  });

  factory BehaviorEntity.fromJson(Map<String, dynamic> json) => BehaviorEntity(
        id: json['id']?.toString() ?? '',
        userId: json['user_id']?.toString() ?? '',
        habits: Map<String, dynamic>.from(json['habits'] ?? {}),
        cognitivePatterns: List<String>.from(json['cognitive_patterns'] ?? []),
        energyLevels: Map<String, double>.from(
          (json['energy_levels'] as Map? ?? {})
              .map((k, v) => MapEntry(k.toString(), (v as num).toDouble())),
        ),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'user_id': userId,
        'habits': habits,
        'cognitive_patterns': cognitivePatterns,
        'energy_levels': energyLevels,
      };
}
