import 'package:flutter/foundation.dart';

@immutable
class ExplainableDecision {
  final String decision;
  final String evidence;
  final double confidence;
  final String alternative;
  final String reason;

  const ExplainableDecision({
    required this.decision,
    required this.evidence,
    required this.confidence,
    required this.alternative,
    required this.reason,
  });

  factory ExplainableDecision.fromJson(Map<String, dynamic> json) =>
      ExplainableDecision(
        decision: json['why_this_resource'] as String? ??
            json['why_this_mission'] as String? ??
            '',
        evidence: json['supporting_gap'] as String? ?? '',
        confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
        alternative: json['alternative_option'] as String? ??
            json['alternative_schedule'] as String? ??
            'None',
        reason: json['why_now'] as String? ??
            json['why_this_time'] as String? ??
            '',
      );

  Map<String, dynamic> toJson() => {
        'why_this_resource': decision,
        'supporting_gap': evidence,
        'confidence': confidence,
        'alternative_option': alternative,
        'why_now': reason,
      };
}

@immutable
class CuratorEntity {
  final Map<String, dynamic> bundle;
  final List<Map<String, dynamic>> candidatesRanked;
  final ExplainableDecision? explanation;

  const CuratorEntity({
    required this.bundle,
    required this.candidatesRanked,
    this.explanation,
  });

  factory CuratorEntity.fromJson(Map<String, dynamic> json) {
    final bundleVal = json['bundle'];
    final bundleMap = bundleVal is Map<String, dynamic> ? bundleVal : null;
    final expJson = json['explanation'] as Map<String, dynamic>? ??
        bundleMap?['explanation'] as Map<String, dynamic>?;
    return CuratorEntity(
      bundle: Map<String, dynamic>.from(json['bundle'] ?? {}),
      candidatesRanked: List<Map<String, dynamic>>.from(
        (json['candidates_ranked'] as List? ?? [])
            .map((e) => Map<String, dynamic>.from(e as Map)),
      ),
      explanation:
          expJson != null ? ExplainableDecision.fromJson(expJson) : null,
    );
  }

  Map<String, dynamic> toJson() => {
        'bundle': bundle,
        'candidates_ranked': candidatesRanked,
        'explanation': explanation?.toJson(),
      };
}
