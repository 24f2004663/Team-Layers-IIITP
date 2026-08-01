import 'notification_service.dart';
import '../workflow/workflow_event.dart';

class WorkflowNotifications {
  final NotificationService _service;

  const WorkflowNotifications(this._service);

  void handleWorkflowEvent(WorkflowEvent event) {
    switch (event) {
      case WorkflowStarted(:final workflowId, :final triggerEvent):
        _service.showLocalNotification(
          title: 'Workflow Triggered',
          body: 'Started $triggerEvent ($workflowId)',
        );
      case WorkflowCompleted(:final workflowId):
        _service.showLocalNotification(
          title: 'Workflow Completed',
          body: 'Workflow $workflowId finished successfully.',
        );
      case AgentFailed(:final agentName, :final error):
        _service.showLocalNotification(
          title: 'Workflow Failed',
          body: 'Agent $agentName failed: $error',
        );
      default:
        break;
    }
  }
}
