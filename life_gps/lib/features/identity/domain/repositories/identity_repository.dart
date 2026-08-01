import '../../../../core/utils/result.dart';
import '../entities/identity_entity.dart';
import '../entities/gap_analysis_entity.dart';

abstract class IdentityRepository {
  Future<Result<IdentityEntity>> getIdentity({bool forceRefresh = false});
  Future<Result<IdentityEntity>> updateIdentity({
    String? archetype,
    List<String>? coreValues,
    List<String>? strengths,
    List<String>? weaknesses,
  });
  Future<Result<GapAnalysisEntity>> getGapAnalysis();
}
