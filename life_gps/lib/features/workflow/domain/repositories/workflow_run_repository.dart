import '../../../../core/utils/result.dart';
import '../entities/workflow_run_entity.dart';

abstract class WorkflowRunRepository {
  Future<Result<WorkflowRunEntity>> triggerWorkflow({
    required String eventType,
    Map<String, dynamic> payload = const {},
  });
  Future<Result<WorkflowRunEntity>> getWorkflowStatus(String id);
  Future<Result<List<WorkflowRunEntity>>> getWorkflowHistory();
}
