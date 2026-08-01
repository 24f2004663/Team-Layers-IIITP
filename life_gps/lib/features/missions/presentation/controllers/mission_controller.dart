import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/mission_entity.dart';
import '../../domain/repositories/mission_repository.dart';
import '../../data/repositories/mission_repository_impl.dart';

final missionRepositoryProvider = Provider<MissionRepository>((ref) {
  return MissionRepositoryImpl(
    ref.watch(apiClientProvider),
    ref.watch(cacheServiceProvider),
  );
});

class MissionController extends AutoDisposeAsyncNotifier<List<MissionEntity>> {
  MissionRepository get _repo => ref.read(missionRepositoryProvider);

  @override
  Future<List<MissionEntity>> build() async {
    final result = await _repo.getMissions();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshMissions() async {
    state = const AsyncLoading();
    final result = await _repo.getMissions(forceRefresh: true);
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final missionControllerProvider =
    AutoDisposeAsyncNotifierProvider<MissionController, List<MissionEntity>>(
  MissionController.new,
);
