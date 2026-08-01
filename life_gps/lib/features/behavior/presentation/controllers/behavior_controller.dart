import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/behavior_entity.dart';
import '../../domain/repositories/behavior_repository.dart';
import '../../data/repositories/behavior_repository_impl.dart';

final behaviorRepositoryProvider = Provider<BehaviorRepository>((ref) {
  return BehaviorRepositoryImpl(
    ref.watch(apiClientProvider),
  );
});

class BehaviorController extends AutoDisposeAsyncNotifier<BehaviorEntity> {
  BehaviorRepository get _repo => ref.read(behaviorRepositoryProvider);

  @override
  Future<BehaviorEntity> build() async {
    final result = await _repo.getBehavior();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshData() async {
    state = const AsyncLoading();
    final result = await _repo.getBehavior();
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final behaviorControllerProvider =
    AutoDisposeAsyncNotifierProvider<BehaviorController, BehaviorEntity>(
  BehaviorController.new,
);
