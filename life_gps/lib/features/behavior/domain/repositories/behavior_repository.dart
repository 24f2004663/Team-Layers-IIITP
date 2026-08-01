import '../../../../core/utils/result.dart';
import '../entities/behavior_entity.dart';

abstract class BehaviorRepository {
  Future<Result<BehaviorEntity>> getBehavior();
}
