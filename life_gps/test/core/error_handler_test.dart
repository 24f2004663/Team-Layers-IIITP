import 'package:flutter_test/flutter_test.dart';
import 'package:life_gps/core/errors/app_exception.dart';
import 'package:life_gps/core/errors/error_handler.dart';
import 'package:dio/dio.dart';

void main() {
  group('ErrorHandler', () {
    test('returns AuthException for 401', () {
      final dioErr = DioException(
        requestOptions: RequestOptions(),
        response: Response(
          requestOptions: RequestOptions(),
          statusCode: 401,
          data: {'message': 'Unauthorized', 'error_code': 'AUTH_ERROR'},
        ),
        type: DioExceptionType.badResponse,
      );
      final result = ErrorHandler.handle(dioErr);
      expect(result, isA<AuthException>());
      expect(result.code, 'AUTH_ERROR');
    });

    test('returns NetworkException on timeout', () {
      final dioErr = DioException(
        requestOptions: RequestOptions(),
        type: DioExceptionType.connectionTimeout,
      );
      final result = ErrorHandler.handle(dioErr);
      expect(result, isA<NetworkException>());
    });

    test('returns ValidationException on 422', () {
      final dioErr = DioException(
        requestOptions: RequestOptions(),
        response: Response(
          requestOptions: RequestOptions(),
          statusCode: 422,
          data: {
            'detail': [
              {
                'loc': ['body', 'email'],
                'msg': 'field required'
              }
            ]
          },
        ),
        type: DioExceptionType.badResponse,
      );
      final result = ErrorHandler.handle(dioErr);
      expect(result, isA<ValidationException>());
    });

    test('passes through AppException unchanged', () {
      const exc = AuthException();
      final result = ErrorHandler.handle(exc);
      expect(result, same(exc));
    });

    test('returns UnknownException for generic errors', () {
      final result = ErrorHandler.handle(Exception('random'));
      expect(result, isA<UnknownException>());
    });
  });
}
