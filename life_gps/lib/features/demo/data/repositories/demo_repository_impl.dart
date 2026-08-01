import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/utils/result.dart';
import '../../domain/repositories/demo_repository.dart';

class DemoRepositoryImpl implements DemoRepository {
  final ApiClient _apiClient;

  const DemoRepositoryImpl(this._apiClient);

  @override
  Future<Result<Map<String, dynamic>>> runDemoProfile(
      String profileName) async {
    try {
      final response = await _apiClient.post<Map<String, dynamic>>(
        AppConfig.demoPath,
        data: {'profile_name': profileName},
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: 'Failed to run demo profile: $profileName',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
