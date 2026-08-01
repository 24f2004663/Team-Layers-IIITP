import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/identity_entity.dart';
import '../../domain/repositories/identity_repository.dart';
import '../../data/repositories/identity_repository_impl.dart';

final identityRepositoryProvider = Provider<IdentityRepository>((ref) {
  return IdentityRepositoryImpl(
    ref.watch(apiClientProvider),
    ref.watch(cacheServiceProvider),
  );
});

class IdentityController extends AutoDisposeAsyncNotifier<IdentityEntity> {
  IdentityRepository get _repo => ref.read(identityRepositoryProvider);

  @override
  Future<IdentityEntity> build() async {
    final result = await _repo.getIdentity();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshData() async {
    state = const AsyncLoading();
    final result = await _repo.getIdentity(forceRefresh: true);
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }

  Future<bool> updateProfile({
    String? archetype,
    List<String>? coreValues,
    List<String>? strengths,
    List<String>? weaknesses,
  }) async {
    state = const AsyncLoading();
    final result = await _repo.updateIdentity(
      archetype: archetype,
      coreValues: coreValues,
      strengths: strengths,
      weaknesses: weaknesses,
    );
    return result.fold(
      onSuccess: (data) {
        state = AsyncValue.data(data);
        return true;
      },
      onFailure: (failure) {
        state = AsyncValue.error(failure, StackTrace.current);
        return false;
      },
    );
  }
}

final identityControllerProvider =
    AutoDisposeAsyncNotifierProvider<IdentityController, IdentityEntity>(
  IdentityController.new,
);
