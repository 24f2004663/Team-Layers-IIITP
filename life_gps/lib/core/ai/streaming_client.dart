import '../services/websocket_service.dart';
import '../workflow/workflow_event.dart';

class StreamingClient {
  final WebSocketService _wsService;

  const StreamingClient(this._wsService);

  Stream<WorkflowEvent> streamWorkflowUpdates(String workflowId) {
    return _wsService.subscribe(workflowId).map((update) {
      if (update.status == 'completed') {
        return WorkflowCompleted(
          workflowId: update.workflowId,
          output: {'completed_agents': update.completedAgents},
        );
      } else if (update.status == 'failed') {
        return AgentFailed(
          workflowId: update.workflowId,
          agentName: update.currentAgent,
          error:
              update.errors.isNotEmpty ? update.errors.first : 'Unknown error',
        );
      } else if (update.currentAgent.isNotEmpty) {
        return AgentStarted(
          workflowId: update.workflowId,
          agentName: update.currentAgent,
        );
      } else {
        return WorkflowProgress(
          workflowId: update.workflowId,
          percentage: update.completionPercentage,
          trace: update.decisionTrace,
        );
      }
    });
  }

  void cancelSubscription() {
    _wsService.dispose();
  }
}
