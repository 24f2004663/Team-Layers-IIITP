/// Sealed hierarchy of application-level exceptions.
sealed class AppException implements Exception {
  final String message;
  final String? code;
  final dynamic details;

  const AppException({
    required this.message,
    this.code,
    this.details,
  });

  @override
  String toString() => 'AppException[$code]: $message';
}

/// 401/403 — user must log in again.
class AuthException extends AppException {
  const AuthException({
    super.message = 'Authentication required. Please log in.',
    super.code = 'AUTH_ERROR',
    super.details,
  });
}

/// Network timeout or no connection.
class NetworkException extends AppException {
  const NetworkException({
    super.message = 'Network error. Please check your connection.',
    super.code = 'NETWORK_ERROR',
    super.details,
  });
}

/// 4xx validation / business logic error from backend.
class ServerException extends AppException {
  final int? statusCode;

  const ServerException({
    required super.message,
    super.code = 'SERVER_ERROR',
    super.details,
    this.statusCode,
  });
}

/// 422 / form validation failures.
class ValidationException extends AppException {
  final Map<String, List<String>>? fieldErrors;

  const ValidationException({
    super.message = 'Validation failed. Please check your input.',
    super.code = 'VALIDATION_ERROR',
    super.details,
    this.fieldErrors,
  });
}

/// Fallback for anything unclassified.
class UnknownException extends AppException {
  const UnknownException({
    super.message = 'An unexpected error occurred.',
    super.code = 'UNKNOWN_ERROR',
    super.details,
  });
}
