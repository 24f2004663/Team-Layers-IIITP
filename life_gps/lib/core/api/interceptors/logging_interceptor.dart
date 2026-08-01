import 'package:dio/dio.dart';
import 'package:logger/logger.dart';

/// Logs every outgoing request and incoming response with timing.
class LoggingInterceptor extends Interceptor {
  final Logger _logger = Logger(
    printer: PrettyPrinter(methodCount: 0, noBoxingByDefault: true),
    level: Level.debug,
  );

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    _logger.d(
      '[REQ] ${options.method} ${options.uri}\n'
      '  Headers: ${_sanitizeHeaders(options.headers)}\n'
      '  Body: ${options.data}',
    );
    options.extra['_startTime'] = DateTime.now().millisecondsSinceEpoch;
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    final start = response.requestOptions.extra['_startTime'] as int?;
    final latency = start != null
        ? '${DateTime.now().millisecondsSinceEpoch - start}ms'
        : '?ms';
    _logger.d(
      '[RES] ${response.statusCode} ${response.requestOptions.uri} ($latency)\n'
      '  Body: ${_truncate(response.data.toString())}',
    );
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    _logger.e(
      '[ERR] ${err.type.name} ${err.requestOptions.uri}\n'
      '  Message: ${err.message}\n'
      '  Response: ${err.response?.data}',
    );
    handler.next(err);
  }

  Map<String, dynamic> _sanitizeHeaders(Map<String, dynamic> headers) {
    final sanitized = Map<String, dynamic>.from(headers);
    if (sanitized.containsKey('Authorization')) {
      sanitized['Authorization'] = 'Bearer [REDACTED]';
    }
    return sanitized;
  }

  String _truncate(String s, {int maxLen = 500}) =>
      s.length > maxLen ? '${s.substring(0, maxLen)}...' : s;
}
