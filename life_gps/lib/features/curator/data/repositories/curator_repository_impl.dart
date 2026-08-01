import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/storage/cache_service.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/curator_entity.dart';
import '../../domain/repositories/curator_repository.dart';

class CuratorRepositoryImpl implements CuratorRepository {
  final ApiClient _apiClient;
  final CacheService _cache;

  const CuratorRepositoryImpl(this._apiClient, this._cache);

  static const String _cacheKey = 'curator_bundle';
  static const Duration _ttl = Duration(minutes: 5);

  @override
  Future<Result<CuratorEntity>> getCuratorBundle(
      {bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _cache.getCachedData(_cacheKey);
      if (cached != null) {
        return Result.success(CuratorEntity.fromJson(cached));
      }
    }

    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.curatorPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheData(_cacheKey, response.data!, _ttl);
        return Result.success(CuratorEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch curator bundle',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<List<Map<String, dynamic>>>> getResources(
      {String? cursor, int limit = 20}) async {
    try {
      final queryParams = <String, dynamic>{'limit': limit};
      if (cursor != null) {
        queryParams['cursor'] = cursor;
      }
      final response = await _apiClient.get<List<dynamic>>(
        AppConfig.resourcesPath,
        queryParameters: queryParams,
      );
      if (response.statusCode == 200 && response.data != null) {
        final list = response.data!
            .map((e) => Map<String, dynamic>.from(e as Map))
            .toList();
        return Result.success(list);
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch resource candidates',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
