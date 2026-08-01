import '../api/api_client.dart';
import '../config/app_config.dart';
import '../utils/result.dart';

class AgentClient {
  final ApiClient _apiClient;

  const AgentClient(this._apiClient);

  Future<Result<Map<String, dynamic>>> getIdentity() async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.identityPath,
      );
      if (response.statusCode == 200) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch identity',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  Future<Result<Map<String, dynamic>>> updateIdentity(
      Map<String, dynamic> data) async {
    try {
      final response = await _apiClient.put<Map<String, dynamic>>(
        AppConfig.identityPath,
        data: data,
      );
      if (response.statusCode == 200) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: 'Failed to update identity',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  Future<Result<Map<String, dynamic>>> getBehavior() async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.behaviorPath,
      );
      if (response.statusCode == 200) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch behavior',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  Future<Result<Map<String, dynamic>>> getGapAnalysis() async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.gapAnalysisPath,
      );
      if (response.statusCode == 200) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch gap analysis',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
