import '../../../../core/utils/result.dart';
import '../entities/planner_entity.dart';

abstract class PlannerRepository {
  Future<Result<PlannerEntity>> getDailyPlan({bool forceRefresh = false});
  Future<Result<PlannerEntity>> getWeeklyPlan({bool forceRefresh = false});
}
