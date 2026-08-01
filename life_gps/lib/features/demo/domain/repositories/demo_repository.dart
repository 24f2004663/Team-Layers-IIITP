import '../../../../core/utils/result.dart';

abstract class DemoRepository {
  Future<Result<Map<String, dynamic>>> runDemoProfile(String profileName);
}
