import 'package:flutter/foundation.dart';

@immutable
class ReflectionEntity {
  final Map<String, dynamic> reflection;
  final Map<String, double> qualityScore;

  const ReflectionEntity({
    required this.reflection,
    required this.qualityScore,
  });

  factory ReflectionEntity.fromJson(Map<String, dynamic> json) =>
      ReflectionEntity(
        reflection: Map<String, dynamic>.from(json['reflection'] ?? {}),
        qualityScore: Map<String, double>.from(
          (json['quality_score'] as Map? ?? {})
              .map((k, v) => MapEntry(k.toString(), (v as num).toDouble())),
        ),
      );
}

@immutable
class LearningLoopEntity {
  final Map<String, dynamic> reflections;
  final Map<String, double> growthDelta;
  final List<Map<String, dynamic>> causalAnalyses;
  final List<Map<String, dynamic>> counterfactuals;
  final Map<String, double> growthIndex;

  const LearningLoopEntity({
    required this.reflections,
    required this.growthDelta,
    required this.causalAnalyses,
    required this.counterfactuals,
    required this.growthIndex,
  });

  factory LearningLoopEntity.fromJson(Map<String, dynamic> json) =>
      LearningLoopEntity(
        reflections: Map<String, dynamic>.from(json['reflections'] ?? {}),
        growthDelta: Map<String, double>.from(
          (json['growth_delta'] as Map? ?? {})
              .map((k, v) => MapEntry(k.toString(), (v as num).toDouble())),
        ),
        causalAnalyses: List<Map<String, dynamic>>.from(
          (json['causal_analyses'] as List? ?? [])
              .map((e) => Map<String, dynamic>.from(e as Map)),
        ),
        counterfactuals: List<Map<String, dynamic>>.from(
          (json['counterfactuals'] as List? ?? [])
              .map((e) => Map<String, dynamic>.from(e as Map)),
        ),
        growthIndex: Map<String, double>.from(
          (json['growth_index'] as Map? ?? {})
              .map((k, v) => MapEntry(k.toString(), (v as num).toDouble())),
        ),
      );
}
