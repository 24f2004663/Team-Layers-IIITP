import 'package:flutter/foundation.dart';

@immutable
sealed class WorkflowState {
  const WorkflowState();
}

class WorkflowIdle extends WorkflowState {
  const WorkflowIdle();
}

class WorkflowQueued extends WorkflowState {
  const WorkflowQueued();
}

class WorkflowRunning extends WorkflowState {
  final String workflowId;
  final double progress;
  final String activeAgent;
  final List<String> logs;
  final List<String> trace;

  const WorkflowRunning({
    required this.workflowId,
    required this.progress,
    required this.activeAgent,
    required this.logs,
    required this.trace,
  });

  WorkflowRunning copyWith({
    double? progress,
    String? activeAgent,
    List<String>? logs,
    List<String>? trace,
  }) =>
      WorkflowRunning(
        workflowId: workflowId,
        progress: progress ?? this.progress,
        activeAgent: activeAgent ?? this.activeAgent,
        logs: logs ?? this.logs,
        trace: trace ?? this.trace,
      );
}

class AgentExecuting extends WorkflowRunning {
  final String agentName;

  const AgentExecuting({
    required super.workflowId,
    required super.progress,
    required super.activeAgent,
    required super.logs,
    required super.trace,
    required this.agentName,
  });
}

class WaitingForUser extends WorkflowRunning {
  final String query;

  const WaitingForUser({
    required super.workflowId,
    required super.progress,
    required super.activeAgent,
    required super.logs,
    required super.trace,
    required this.query,
  });
}

class Completed extends WorkflowState {
  final String workflowId;
  final Map<String, dynamic> result;

  const Completed({required this.workflowId, required this.result});
}

class Failed extends WorkflowState {
  final String workflowId;
  final String error;

  const Failed({required this.workflowId, required this.error});
}

class Cancelled extends WorkflowState {
  final String workflowId;

  const Cancelled({required this.workflowId});
}
