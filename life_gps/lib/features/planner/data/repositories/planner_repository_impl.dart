import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/storage/cache_service.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/planner_entity.dart';
import '../../domain/repositories/planner_repository.dart';

class PlannerRepositoryImpl implements PlannerRepository {
  final ApiClient _apiClient;
  final CacheService _cache;

  const PlannerRepositoryImpl(this._apiClient, this._cache);

  static const String _dailyCacheKey = 'planner_daily';
  static const String _weeklyCacheKey = 'planner_weekly';
  static const Duration _ttl = Duration(minutes: 5);

  @override
  Future<Result<PlannerEntity>> getDailyPlan(
      {bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _cache.getCachedData(_dailyCacheKey);
      if (cached != null) {
        return Result.success(PlannerEntity.fromJson(cached));
      }
    }

    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.plannerDailyPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheData(_dailyCacheKey, response.data!, _ttl);
        return Result.success(PlannerEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch daily plan',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<PlannerEntity>> getWeeklyPlan(
      {bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _cache.getCachedData(_weeklyCacheKey);
      if (cached != null) {
        return Result.success(PlannerEntity.fromJson(cached));
      }
    }

    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.plannerWeeklyPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheData(_weeklyCacheKey, response.data!, _ttl);
        return Result.success(PlannerEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch weekly plan',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
