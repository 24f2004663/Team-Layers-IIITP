import '../../../../core/ai/ai_client.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/workflow_run_entity.dart';
import '../../domain/repositories/workflow_run_repository.dart';

class WorkflowRunRepositoryImpl implements WorkflowRunRepository {
  final AiClient _aiClient;

  const WorkflowRunRepositoryImpl(this._aiClient);

  @override
  Future<Result<WorkflowRunEntity>> triggerWorkflow({
    required String eventType,
    Map<String, dynamic> payload = const {},
  }) async {
    final result = await _aiClient.workflow.triggerWorkflow(
      eventType: eventType,
      payload: payload,
    );
    return result.fold(
      onSuccess: (data) => Result.success(WorkflowRunEntity.fromJson(data)),
      onFailure: (failure) => Result.failure(failure),
    );
  }

  @override
  Future<Result<WorkflowRunEntity>> getWorkflowStatus(String id) async {
    final result = await _aiClient.workflow.getWorkflowStatus(id);
    return result.fold(
      onSuccess: (data) => Result.success(WorkflowRunEntity.fromJson(data)),
      onFailure: (failure) => Result.failure(failure),
    );
  }

  @override
  Future<Result<List<WorkflowRunEntity>>> getWorkflowHistory() async {
    final result = await _aiClient.workflow.getWorkflowHistory();
    return result.fold(
      onSuccess: (data) => Result.success(
        data
            .map((e) => WorkflowRunEntity.fromJson(e as Map<String, dynamic>))
            .toList(),
      ),
      onFailure: (failure) => Result.failure(failure),
    );
  }
}
