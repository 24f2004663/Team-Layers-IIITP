import 'dart:async';
import 'package:dio/dio.dart';

/// Retries failed requests on transient errors with exponential backoff.
class RetryInterceptor extends Interceptor {
  final Dio dio;
  final int maxRetries;
  final int baseDelayMs;

  static const _retryableStatuses = {500, 502, 503, 504};

  RetryInterceptor({
    required this.dio,
    this.maxRetries = 3,
    this.baseDelayMs = 500,
  });

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final attempt = err.requestOptions.extra['_retryAttempt'] as int? ?? 0;

    final shouldRetry = _shouldRetry(err, attempt);
    if (!shouldRetry) {
      return handler.next(err);
    }

    final nextAttempt = attempt + 1;
    final delayMs =
        baseDelayMs * (1 << attempt); // exponential: 500, 1000, 2000
    await Future.delayed(Duration(milliseconds: delayMs));

    final retryOptions = err.requestOptions.copyWith(
      extra: {...err.requestOptions.extra, '_retryAttempt': nextAttempt},
    );

    try {
      final response = await dio.fetch(retryOptions);
      handler.resolve(response);
    } on DioException catch (retryErr) {
      handler.next(retryErr);
    }
  }

  bool _shouldRetry(DioException err, int attempt) {
    if (attempt >= maxRetries) return false;
    if (err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.sendTimeout ||
        err.type == DioExceptionType.connectionError) {
      return true;
    }
    final statusCode = err.response?.statusCode;
    return statusCode != null && _retryableStatuses.contains(statusCode);
  }
}
