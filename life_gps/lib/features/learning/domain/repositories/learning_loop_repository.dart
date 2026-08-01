import '../../../../core/utils/result.dart';
import '../entities/learning_loop_entity.dart';

abstract class LearningLoopRepository {
  Future<Result<ReflectionEntity>> getReflection();
  Future<Result<LearningLoopEntity>> getLearningLoop();
}
