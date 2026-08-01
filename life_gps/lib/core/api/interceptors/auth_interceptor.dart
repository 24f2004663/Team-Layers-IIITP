import 'package:dio/dio.dart';
import '../../constants/app_constants.dart';
import '../../storage/secure_storage.dart';

/// Injects JWT Bearer token on every outgoing request.
/// On 401 response, clears the stored token.
class AuthInterceptor extends Interceptor {
  final SecureStorageService _storage;

  /// Callback invoked when a 401 is received — used to trigger nav to /login.
  final void Function()? onUnauthorized;

  AuthInterceptor({
    required SecureStorageService storage,
    this.onUnauthorized,
  }) : _storage = storage;

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await _storage.getToken();
    if (token != null && token.isNotEmpty) {
      options.headers[AppConstants.authorizationHeader] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (response.statusCode == 401) {
      _storage.deleteToken();
      onUnauthorized?.call();
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      _storage.deleteToken();
      onUnauthorized?.call();
    }
    handler.next(err);
  }
}
