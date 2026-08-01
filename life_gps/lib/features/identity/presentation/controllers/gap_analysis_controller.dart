import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/gap_analysis_entity.dart';
import '../../domain/repositories/identity_repository.dart';
import 'identity_controller.dart';

class GapAnalysisController
    extends AutoDisposeAsyncNotifier<GapAnalysisEntity> {
  IdentityRepository get _repo => ref.read(identityRepositoryProvider);

  @override
  Future<GapAnalysisEntity> build() async {
    final result = await _repo.getGapAnalysis();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshData() async {
    state = const AsyncLoading();
    final result = await _repo.getGapAnalysis();
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final gapAnalysisControllerProvider =
    AutoDisposeAsyncNotifierProvider<GapAnalysisController, GapAnalysisEntity>(
  GapAnalysisController.new,
);
