import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/storage/cache_service.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/mission_entity.dart';
import '../../domain/repositories/mission_repository.dart';

class MissionRepositoryImpl implements MissionRepository {
  final ApiClient _apiClient;
  final CacheService _cache;

  const MissionRepositoryImpl(this._apiClient, this._cache);

  static const String _cacheKey = 'missions_list';
  static const Duration _ttl = Duration(minutes: 5);

  @override
  Future<Result<List<MissionEntity>>> getMissions(
      {bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _cache.getCachedListData(_cacheKey);
      if (cached != null) {
        return Result.success(cached
            .map((e) => MissionEntity.fromJson(e as Map<String, dynamic>))
            .toList());
      }
    }

    try {
      final response = await _apiClient.get<List<dynamic>>(
        AppConfig.missionsPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheListData(_cacheKey, response.data!, _ttl);
        return Result.success(response.data!
            .map((e) => MissionEntity.fromJson(e as Map<String, dynamic>))
            .toList());
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch missions list',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
