import '../../../../core/utils/result.dart';
import '../entities/dashboard_entity.dart';

abstract class DashboardRepository {
  Future<Result<DashboardFullEntity>> getDashboardData(
      {bool forceRefresh = false});
  Future<Result<DashboardSummaryEntity>> getSummary(
      {bool forceRefresh = false});
  Future<Result<DashboardTodayEntity>> getToday({bool forceRefresh = false});
  Future<Result<DashboardProgressEntity>> getProgress(
      {bool forceRefresh = false});
  Future<Result<DashboardFutureEntity>> getFuture({bool forceRefresh = false});
}
