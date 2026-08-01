/// App configuration — environment-aware API settings.
/// Reads from compile-time String.fromEnvironment or falls back to dev defaults.
class AppConfig {
  static const String _envBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:9000',
  );

  static const String _envWsUrl = String.fromEnvironment(
    'WS_BASE_URL',
    defaultValue: 'ws://localhost:9000',
  );

  static const String _envEnvironment = String.fromEnvironment(
    'APP_ENV',
    defaultValue: 'development',
  );

  // ─── API ──────────────────────────────────────────────────────────────────
  static String get baseUrl => _envBaseUrl;
  static String get wsUrl => _envWsUrl;
  static String get apiVersion => 'v1';
  static String get apiPrefix => '/api/$apiVersion';
  static String get fullApiBase => '$baseUrl$apiPrefix';

  // ─── WebSocket ────────────────────────────────────────────────────────────
  static String get wsWorkflowEndpoint => '$wsUrl/ws/workflow';

  // ─── Auth Endpoints ───────────────────────────────────────────────────────
  static String get loginPath => '/auth/login';
  static String get registerPath => '/auth/register';
  static String get mePath => '/users/me';

  // ─── Feature Endpoints ───────────────────────────────────────────────────
  static String get dashboardPath => '/dashboard';
  static String get identityPath => '/identity';
  static String get behaviorPath => '/behavior';
  static String get gapAnalysisPath => '/gap-analysis';
  static String get missionsPath => '/missions';
  static String get plannerDailyPath => '/planner/daily';
  static String get plannerWeeklyPath => '/planner/weekly';
  static String get curatorPath => '/curator';
  static String get resourcesPath => '/resources';
  static String get reflectionPath => '/reflection';
  static String get learningLoopPath => '/learning-loop';
  static String get workflowsPath => '/workflows';
  static String get demoPath => '/demo/run';

  // ─── HTTP Config ──────────────────────────────────────────────────────────
  static const Duration connectTimeout = Duration(seconds: 15);
  static const Duration receiveTimeout = Duration(seconds: 30);
  static const Duration sendTimeout = Duration(seconds: 15);
  static const int maxRetries = 3;
  static const int retryBaseDelayMs = 500;

  // ─── WebSocket Config ────────────────────────────────────────────────────
  static const int wsMaxReconnectAttempts = 5;
  static const Duration wsReconnectBaseDelay = Duration(seconds: 2);

  // ─── Environment ─────────────────────────────────────────────────────────
  static String get environment => _envEnvironment;
  static bool get isDevelopment => _envEnvironment == 'development';
  static bool get isProduction => _envEnvironment == 'production';
  static bool get isTesting => _envEnvironment == 'testing';
}
