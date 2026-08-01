import 'package:dio/dio.dart';
import 'app_exception.dart';

/// Maps Dio errors and backend response envelopes into [AppException] subtypes.
class ErrorHandler {
  const ErrorHandler._();

  static AppException handle(Object error) {
    if (error is AppException) return error;

    if (error is DioException) {
      return _handleDioException(error);
    }

    return UnknownException(details: error.toString());
  }

  static AppException _handleDioException(DioException err) {
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const NetworkException(
          message: 'Request timed out. Please try again.',
          code: 'TIMEOUT',
        );
      case DioExceptionType.connectionError:
        return const NetworkException(
          message: 'Cannot connect to the server. Check your network.',
          code: 'CONNECTION_ERROR',
        );
      case DioExceptionType.badResponse:
        return _handleBadResponse(err);
      case DioExceptionType.cancel:
        return const NetworkException(
          message: 'Request was cancelled.',
          code: 'CANCELLED',
        );
      default:
        return UnknownException(details: err.message);
    }
  }

  static AppException _handleBadResponse(DioException err) {
    final statusCode = err.response?.statusCode;
    final data = err.response?.data;

    // Parse backend standard error envelope
    String message = 'Server error occurred.';
    String? code;
    dynamic details;

    if (data is Map<String, dynamic>) {
      final msgVal = data['message'];
      final detailVal = data['detail'];
      if (msgVal is String) {
        message = msgVal;
      } else if (detailVal is String) {
        message = detailVal;
      } else if (detailVal is List) {
        message =
            'Validation failed: ${detailVal.map((e) => e is Map ? e['msg'] : e.toString()).join(', ')}';
      }
      code = data['error_code']?.toString() ?? data['code']?.toString();
      details = data['details'];
    }

    switch (statusCode) {
      case 401:
      case 403:
        return AuthException(
            message: message, code: code ?? 'AUTH_ERROR', details: details);
      case 422:
        final fieldErrors = _parseFieldErrors(data);
        return ValidationException(
          message: message,
          code: code ?? 'VALIDATION_ERROR',
          details: details,
          fieldErrors: fieldErrors,
        );
      case 400:
        return ServerException(
          message: message,
          code: code ?? 'BAD_REQUEST',
          details: details,
          statusCode: statusCode,
        );
      case 404:
        return ServerException(
          message: message,
          code: code ?? 'NOT_FOUND',
          details: details,
          statusCode: statusCode,
        );
      default:
        return ServerException(
          message: message,
          code: code ?? 'SERVER_ERROR',
          details: details,
          statusCode: statusCode,
        );
    }
  }

  static Map<String, List<String>>? _parseFieldErrors(dynamic data) {
    if (data is! Map<String, dynamic>) return null;
    final detail = data['detail'];
    if (detail is! List) return null;
    final result = <String, List<String>>{};
    for (final item in detail) {
      if (item is Map<String, dynamic>) {
        final loc = (item['loc'] as List?)?.lastOrNull?.toString() ?? 'field';
        final msg = item['msg']?.toString() ?? 'Invalid';
        result.putIfAbsent(loc, () => []).add(msg);
      }
    }
    return result.isEmpty ? null : result;
  }
}
