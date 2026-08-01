import '../../../../core/utils/result.dart';
import '../entities/mission_entity.dart';

abstract class MissionRepository {
  Future<Result<List<MissionEntity>>> getMissions({bool forceRefresh = false});
}
