class AnalyticsMetric {
  final String key;
  final double value;
  final DateTime timestamp;

  const AnalyticsMetric({
    required this.key,
    required this.value,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() => {
        'key': key,
        'value': value,
        'timestamp': timestamp.toIso8601String(),
      };
}
