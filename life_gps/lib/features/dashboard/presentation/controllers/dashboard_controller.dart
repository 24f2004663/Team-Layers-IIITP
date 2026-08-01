import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/dashboard_entity.dart';
import '../../domain/repositories/dashboard_repository.dart';
import '../../data/repositories/dashboard_repository_impl.dart';

final dashboardRepositoryProvider = Provider<DashboardRepository>((ref) {
  return DashboardRepositoryImpl(
    ref.watch(apiClientProvider),
    ref.watch(cacheServiceProvider),
  );
});

class DashboardController
    extends AutoDisposeAsyncNotifier<DashboardFullEntity> {
  DashboardRepository get _repo => ref.read(dashboardRepositoryProvider);

  @override
  Future<DashboardFullEntity> build() async {
    final result = await _repo.getDashboardData();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshData() async {
    state = const AsyncLoading();
    final result = await _repo.getDashboardData(forceRefresh: true);
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final dashboardControllerProvider =
    AutoDisposeAsyncNotifierProvider<DashboardController, DashboardFullEntity>(
  DashboardController.new,
);
