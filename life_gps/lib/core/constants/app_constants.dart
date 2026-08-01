/// App-wide constants.
class AppConstants {
  AppConstants._();

  // Storage keys
  static const String tokenKey = 'life_gps_access_token';
  static const String userKey = 'life_gps_user';
  static const String themeKey = 'life_gps_theme_mode';
  static const String onboardingKey = 'life_gps_onboarding_complete';

  // HTTP Headers
  static const String authorizationHeader = 'Authorization';
  static const String contentTypeHeader = 'Content-Type';
  static const String correlationIdHeader = 'X-Correlation-ID';
  static const String requestIdHeader = 'X-Request-ID';

  // App
  static const String appName = 'Life-GPS';
  static const String appVersion = '1.0.0';
  static const String appTagline = 'Your AI-Powered Life Operating System';

  // Pagination
  static const int defaultPageSize = 20;

  // Animation durations
  static const Duration shortAnimation = Duration(milliseconds: 200);
  static const Duration mediumAnimation = Duration(milliseconds: 400);
  static const Duration longAnimation = Duration(milliseconds: 700);

  // Timeouts
  static const Duration splashDuration = Duration(seconds: 2);
}
