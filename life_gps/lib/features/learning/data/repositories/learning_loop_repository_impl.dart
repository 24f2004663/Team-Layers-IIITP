import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/learning_loop_entity.dart';
import '../../domain/repositories/learning_loop_repository.dart';

class LearningLoopRepositoryImpl implements LearningLoopRepository {
  final ApiClient _apiClient;

  const LearningLoopRepositoryImpl(this._apiClient);

  @override
  Future<Result<ReflectionEntity>> getReflection() async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.reflectionPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(ReflectionEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch reflections',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<LearningLoopEntity>> getLearningLoop() async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.learningLoopPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(LearningLoopEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch learning loop indices',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
