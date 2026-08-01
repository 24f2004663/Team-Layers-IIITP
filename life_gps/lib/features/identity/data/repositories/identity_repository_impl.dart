import '../../../../core/api/api_client.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/storage/cache_service.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/identity_entity.dart';
import '../../domain/entities/gap_analysis_entity.dart';
import '../../domain/repositories/identity_repository.dart';

class IdentityRepositoryImpl implements IdentityRepository {
  final ApiClient _apiClient;
  final CacheService _cache;

  const IdentityRepositoryImpl(this._apiClient, this._cache);

  static const String _cacheKey = 'identity_data';
  static const String _gapCacheKey = 'gap_analysis_data';
  static const Duration _ttl = Duration(minutes: 10);

  @override
  Future<Result<GapAnalysisEntity>> getGapAnalysis() async {
    final cached = _cache.getCachedData(_gapCacheKey);
    if (cached != null) {
      return Result.success(GapAnalysisEntity.fromJson(cached));
    }

    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.gapAnalysisPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheData(_gapCacheKey, response.data!, _ttl);
        return Result.success(GapAnalysisEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to fetch gap analysis',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<IdentityEntity>> getIdentity(
      {bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _cache.getCachedData(_cacheKey);
      if (cached != null) {
        return Result.success(IdentityEntity.fromJson(cached));
      }
    }

    try {
      final response = await _apiClient.get<Map<String, dynamic>>(
        AppConfig.identityPath,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.cacheData(_cacheKey, response.data!, _ttl);
        return Result.success(IdentityEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Identity profile not found',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }

  @override
  Future<Result<IdentityEntity>> updateIdentity({
    String? archetype,
    List<String>? coreValues,
    List<String>? strengths,
    List<String>? weaknesses,
  }) async {
    final payload = <String, dynamic>{};
    if (archetype != null) payload['archetype'] = archetype;
    if (coreValues != null) payload['core_values'] = coreValues;
    if (strengths != null) payload['strengths'] = strengths;
    if (weaknesses != null) payload['weaknesses'] = weaknesses;

    try {
      final response = await _apiClient.put<Map<String, dynamic>>(
        AppConfig.identityPath,
        data: payload,
      );
      if (response.statusCode == 200 && response.data != null) {
        await _cache.invalidateCache(_cacheKey);
        return Result.success(IdentityEntity.fromJson(response.data!));
      }
      return Result.failure(ServerFailure(
        message: 'Failed to update identity profile',
        statusCode: response.statusCode,
      ));
    } catch (e) {
      return Result.failure(NetworkFailure(e.toString()));
    }
  }
}
