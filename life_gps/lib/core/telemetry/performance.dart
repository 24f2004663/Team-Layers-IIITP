class PerformanceTelemetry {
  final Map<String, Stopwatch> _timers = {};
  final List<Map<String, dynamic>> latencyLogs = [];

  void startTrace(String name) {
    _timers[name] = Stopwatch()..start();
  }

  void endTrace(String name) {
    final watch = _timers[name];
    if (watch != null) {
      watch.stop();
      latencyLogs.add({
        'trace_name': name,
        'duration_ms': watch.elapsedMilliseconds,
        'timestamp': DateTime.now().toIso8601String(),
      });
      _timers.remove(name);
    }
  }
}
