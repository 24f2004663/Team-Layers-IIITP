import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/storage/cache_service.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/dashboard_entity.dart';
import '../../domain/repositories/dashboard_repository.dart';

class DashboardRepositoryImpl implements DashboardRepository {
  final ApiClient _apiClient;
  final CacheService _cache;

  const DashboardRepositoryImpl(this._apiClient, this._cache);

  static const String _cacheKey = 'dashboard_full';
  static const Duration _ttl = Duration(minutes: 5);

  @override
  Future<Result<DashboardFullEntity>> getDashboardData(
      {bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _cache.getCachedData(_cacheKey);
      if (cached != null) {
        return Result.success(DashboardFullEntity.fromJson(cached));
      }
    }

    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.dashboardPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheData(_cacheKey, response.data!, _ttl);
        return Result.success(DashboardFullEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch dashboard data',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<DashboardSummaryEntity>> getSummary(
      {bool forceRefresh = false}) async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        '${AppConfig.dashboardPath}/summary',
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(DashboardSummaryEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch summary',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<DashboardTodayEntity>> getToday(
      {bool forceRefresh = false}) async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        '${AppConfig.dashboardPath}/today',
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(DashboardTodayEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch today agenda',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<DashboardProgressEntity>> getProgress(
      {bool forceRefresh = false}) async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        '${AppConfig.dashboardPath}/progress',
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(DashboardProgressEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch progress metrics',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<DashboardFutureEntity>> getFuture(
      {bool forceRefresh = false}) async {
    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        '${AppConfig.dashboardPath}/future',
      );
      if (response.statusCode == 200 && response.data != null) {
        return Result.success(DashboardFutureEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch future trajectory',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
