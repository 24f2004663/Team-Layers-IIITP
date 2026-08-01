import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/behavior_entity.dart';
import '../../domain/repositories/behavior_repository.dart';

class BehaviorRepositoryImpl implements BehaviorRepository {
  final ApiClient _apiClient;

  const BehaviorRepositoryImpl(this._apiClient);

  @override
  Future<Result<BehaviorEntity>> getBehavior() async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.behaviorPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(BehaviorEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Behavior profile not found',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
