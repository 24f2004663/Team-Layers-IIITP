import 'package:flutter/foundation.dart';

@immutable
class WorkflowRunEntity {
  final String id;
  final String status;
  final String currentAgent;
  final List<String> completedAgents;
  final List<String> failedAgents;
  final List<String> errors;
  final double completionPercentage;

  const WorkflowRunEntity({
    required this.id,
    required this.status,
    required this.currentAgent,
    required this.completedAgents,
    required this.failedAgents,
    required this.errors,
    required this.completionPercentage,
  });

  factory WorkflowRunEntity.fromJson(Map<String, dynamic> json) =>
      WorkflowRunEntity(
        id: json['workflow_id']?.toString() ?? '',
        status: json['status'] as String? ?? 'pending',
        currentAgent: json['current_agent'] as String? ?? '',
        completedAgents: List<String>.from(json['completed_agents'] ?? []),
        failedAgents: List<String>.from(json['failed_agents'] ?? []),
        errors: List<String>.from(json['errors'] ?? []),
        completionPercentage:
            (json['completion_percentage'] as num?)?.toDouble() ?? 0.0,
      );

  Map<String, dynamic> toJson() => {
        'workflow_id': id,
        'status': status,
        'current_agent': currentAgent,
        'completed_agents': completedAgents,
        'failed_agents': failedAgents,
        'errors': errors,
        'completion_percentage': completionPercentage,
      };
}
