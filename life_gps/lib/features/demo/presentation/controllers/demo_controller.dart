import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../domain/repositories/demo_repository.dart';
import '../../data/repositories/demo_repository_impl.dart';

final demoRepositoryProvider = Provider<DemoRepository>((ref) {
  return DemoRepositoryImpl(
    ref.watch(apiClientProvider),
  );
});

class DemoController extends AutoDisposeAsyncNotifier<Map<String, dynamic>?> {
  DemoRepository get _repo => ref.read(demoRepositoryProvider);

  @override
  Future<Map<String, dynamic>?> build() async {
    return null;
  }

  Future<bool> runProfile(String profileName) async {
    state = const AsyncLoading();
    final result = await _repo.runDemoProfile(profileName);
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

final demoControllerProvider =
    AutoDisposeAsyncNotifierProvider<DemoController, Map<String, dynamic>?>(
  DemoController.new,
);
