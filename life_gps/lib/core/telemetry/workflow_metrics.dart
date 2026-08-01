class WorkflowMetricsTelemetry {
  final List<Map<String, dynamic>> executionLogs = [];

  void logWorkflowRun({
    required String workflowId,
    required String triggerEvent,
    required int durationMs,
    required String finalStatus,
  }) {
    executionLogs.add({
      'workflow_id': workflowId,
      'trigger_event': triggerEvent,
      'duration_ms': durationMs,
      'final_status': finalStatus,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
}
