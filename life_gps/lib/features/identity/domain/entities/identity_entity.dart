import 'package:flutter/foundation.dart';

@immutable
class IdentityEntity {
  final String id;
  final String userId;
  final String archetype;
  final List<String> coreValues;
  final List<String> strengths;
  final List<String> weaknesses;

  const IdentityEntity({
    required this.id,
    required this.userId,
    required this.archetype,
    required this.coreValues,
    required this.strengths,
    required this.weaknesses,
  });

  factory IdentityEntity.fromJson(Map<String, dynamic> json) => IdentityEntity(
        id: json['id']?.toString() ?? '',
        userId: json['user_id']?.toString() ?? '',
        archetype: json['archetype'] as String? ?? 'Explorer',
        coreValues: List<String>.from(json['core_values'] ?? []),
        strengths: List<String>.from(json['strengths'] ?? []),
        weaknesses: List<String>.from(json['weaknesses'] ?? []),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'user_id': userId,
        'archetype': archetype,
        'core_values': coreValues,
        'strengths': strengths,
        'weaknesses': weaknesses,
      };
}
