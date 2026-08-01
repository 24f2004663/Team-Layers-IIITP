import '../api/api_client.dart';
import '../config/app_config.dart';
import '../utils/result.dart';

class WorkflowClient {
  final ApiClient _apiClient;

  const WorkflowClient(this._apiClient);

  Future<Result<Map<String, dynamic>>> triggerWorkflow({
    required String eventType,
    Map<String, dynamic> payload = const {},
  }) async {
    try {
      final response = await _apiClient.post<Map<String, dynamic>>(
        AppConfig.workflowsPath,
        data: {'event_type': eventType, 'payload': payload},
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: response.statusMessage ?? 'Failed to trigger workflow',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  Future<Result<Map<String, dynamic>>> triggerDemoRun(String profileName) async {
    try {
      final response = await _apiClient.post<Map<String, dynamic>>(
        AppConfig.demoPath,
        data: {'profile_name': profileName},
      );
      if (response.statusCode == 200 || response.statusCode == 201 || response.statusCode == 202) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: response.statusMessage ?? 'Failed to trigger demo run',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  Future<Result<Map<String, dynamic>>> getWorkflowStatus(String id) async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        '${AppConfig.workflowsPath}/$id',
      );
      if (response.statusCode == 200) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: response.statusMessage ?? 'Failed to fetch workflow status',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  Future<Result<List<dynamic>>> getWorkflowHistory() async {
    try {
      final response = await _apiClient.get<List<dynamic>>(
        AppConfig.workflowsPath,
      );
      if (response.statusCode == 200) {
        return Result.success(response.data!);
      }
      return Result.failure(ServerFailure(
        message: response.statusMessage ?? 'Failed to fetch workflow history',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
