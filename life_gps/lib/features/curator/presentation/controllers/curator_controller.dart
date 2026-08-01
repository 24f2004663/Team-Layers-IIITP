import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/curator_entity.dart';
import '../../domain/repositories/curator_repository.dart';
import '../../data/repositories/curator_repository_impl.dart';

final curatorRepositoryProvider = Provider<CuratorRepository>((ref) {
  return CuratorRepositoryImpl(
    ref.watch(apiClientProvider),
    ref.watch(cacheServiceProvider),
  );
});

class CuratorController extends AutoDisposeAsyncNotifier<CuratorEntity> {
  CuratorRepository get _repo => ref.read(curatorRepositoryProvider);

  @override
  Future<CuratorEntity> build() async {
    final result = await _repo.getCuratorBundle();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshBundle() async {
    state = const AsyncLoading();
    final result = await _repo.getCuratorBundle(forceRefresh: true);
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final curatorControllerProvider =
    AutoDisposeAsyncNotifierProvider<CuratorController, CuratorEntity>(
  CuratorController.new,
);
