import 'package:flutter/foundation.dart';

@immutable
sealed class WorkflowEvent {
  final String workflowId;
  const WorkflowEvent(this.workflowId);
}

class WorkflowStarted extends WorkflowEvent {
  final String triggerEvent;
  const WorkflowStarted(
      {required String workflowId, required this.triggerEvent})
      : super(workflowId);
}

class WorkflowProgress extends WorkflowEvent {
  final double percentage;
  final List<String> trace;
  const WorkflowProgress({
    required String workflowId,
    required this.percentage,
    required this.trace,
  }) : super(workflowId);
}

class AgentStarted extends WorkflowEvent {
  final String agentName;
  const AgentStarted({required String workflowId, required this.agentName})
      : super(workflowId);
}

class AgentCompleted extends WorkflowEvent {
  final String agentName;
  final Map<String, dynamic>? output;
  const AgentCompleted({
    required String workflowId,
    required this.agentName,
    this.output,
  }) : super(workflowId);
}

class AgentFailed extends WorkflowEvent {
  final String agentName;
  final String error;
  const AgentFailed({
    required String workflowId,
    required this.agentName,
    required this.error,
  }) : super(workflowId);
}

class WorkflowCompleted extends WorkflowEvent {
  final Map<String, dynamic> output;
  const WorkflowCompleted({required String workflowId, required this.output})
      : super(workflowId);
}

class WorkflowCancelled extends WorkflowEvent {
  const WorkflowCancelled({required String workflowId}) : super(workflowId);
}

class Heartbeat extends WorkflowEvent {
  final DateTime timestamp;
  const Heartbeat({required String workflowId, required this.timestamp})
      : super(workflowId);
}
