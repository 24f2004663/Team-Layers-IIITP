import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/planner_entity.dart';
import '../../domain/repositories/planner_repository.dart';
import '../../data/repositories/planner_repository_impl.dart';

final plannerRepositoryProvider = Provider<PlannerRepository>((ref) {
  return PlannerRepositoryImpl(
    ref.watch(apiClientProvider),
    ref.watch(cacheServiceProvider),
  );
});

class PlannerController extends AutoDisposeAsyncNotifier<PlannerEntity> {
  PlannerRepository get _repo => ref.read(plannerRepositoryProvider);

  @override
  Future<PlannerEntity> build() async {
    final result = await _repo.getDailyPlan();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshPlan({bool weekly = false}) async {
    state = const AsyncLoading();
    final result = weekly
        ? await _repo.getWeeklyPlan(forceRefresh: true)
        : await _repo.getDailyPlan(forceRefresh: true);
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final plannerControllerProvider =
    AutoDisposeAsyncNotifierProvider<PlannerController, PlannerEntity>(
  PlannerController.new,
);
