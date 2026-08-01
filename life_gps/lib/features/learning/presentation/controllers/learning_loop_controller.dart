import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/learning_loop_entity.dart';
import '../../domain/repositories/learning_loop_repository.dart';
import '../../data/repositories/learning_loop_repository_impl.dart';

final learningLoopRepositoryProvider = Provider<LearningLoopRepository>((ref) {
  return LearningLoopRepositoryImpl(
    ref.watch(apiClientProvider),
  );
});

class LearningLoopController
    extends AutoDisposeAsyncNotifier<LearningLoopEntity> {
  LearningLoopRepository get _repo => ref.read(learningLoopRepositoryProvider);

  @override
  Future<LearningLoopEntity> build() async {
    final result = await _repo.getLearningLoop();
    return result.fold(
      onSuccess: (data) => data,
      onFailure: (failure) => throw failure,
    );
  }

  Future<void> refreshLoop() async {
    state = const AsyncLoading();
    final result = await _repo.getLearningLoop();
    state = result.fold(
      onSuccess: (data) => AsyncValue.data(data),
      onFailure: (failure) => AsyncValue.error(failure, StackTrace.current),
    );
  }
}

final learningLoopControllerProvider = AutoDisposeAsyncNotifierProvider<
    LearningLoopController, LearningLoopEntity>(
  LearningLoopController.new,
);
