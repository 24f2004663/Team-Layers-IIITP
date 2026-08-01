import '../../../../core/utils/result.dart';
import '../entities/curator_entity.dart';

abstract class CuratorRepository {
  Future<Result<CuratorEntity>> getCuratorBundle({bool forceRefresh = false});
  Future<Result<List<Map<String, dynamic>>>> getResources(
      {String? cursor, int limit = 20});
}
