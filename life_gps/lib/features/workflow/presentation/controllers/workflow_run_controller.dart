import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/workflow_run_entity.dart';
import '../../domain/repositories/workflow_run_repository.dart';
import '../../data/repositories/workflow_run_repository_impl.dart';

final workflowRunRepositoryProvider = Provider<WorkflowRunRepository>((ref) {
  return WorkflowRunRepositoryImpl(
    ref.watch(aiClientProvider),
  );
});

class WorkflowHistoryController
    extends AutoDisposeAsyncNotifier<List<WorkflowRunEntity>> {
  WorkflowRunRepository get _repo => ref.read(workflowRunRepositoryProvider);

  @override
  Future<List<WorkflowRunEntity>> build() async {
    final result = await _repo.getWorkflowHistory();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshHistory() async {
    state = const AsyncLoading();
    final result = await _repo.getWorkflowHistory();
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final workflowHistoryControllerProvider = AutoDisposeAsyncNotifierProvider<
    WorkflowHistoryController, List<WorkflowRunEntity>>(
  WorkflowHistoryController.new,
);
