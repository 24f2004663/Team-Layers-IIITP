class CrashTelemetry {
  final List<Map<String, dynamic>> errors = [];

  void reportError(Object error, StackTrace? stack) {
    errors.add({
      'error': error.toString(),
      'stack': stack?.toString(),
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
}
