import 'package:flutter_test/flutter_test.dart';
import 'package:life_gps/core/utils/result.dart';

void main() {
  group('Result and Failure Pattern', () {
    test('Success returns true for isSuccess and false for isFailure', () {
      const result = Success<int>(42);
      expect(result.isSuccess, isTrue);
      expect(result.isFailure, isFalse);
      expect(result.valueOrNull, 42);
      expect(result.failureOrNull, isNull);
    });

    test('Failure returns true for isFailure and false for isSuccess', () {
      const result = FailureResult<int>(NetworkFailure('No connection'));
      expect(result.isSuccess, isFalse);
      expect(result.isFailure, isTrue);
      expect(result.valueOrNull, isNull);
      expect(result.failureOrNull, isA<NetworkFailure>());
    });

    test('fold routes correctly on Success', () {
      const result = Success<String>('value');
      final stringResult = result.fold(
        onSuccess: (val) => 'Success: $val',
        onFailure: (fail) => 'Failure',
      );
      expect(stringResult, 'Success: value');
    });

    test('fold routes correctly on Failure', () {
      const result = FailureResult<String>(AuthFailure('Expired'));
      final stringResult = result.fold(
        onSuccess: (val) => 'Success',
        onFailure: (fail) => 'Failure: ${fail.message}',
      );
      expect(stringResult, 'Failure: Expired');
    });
  });
}
