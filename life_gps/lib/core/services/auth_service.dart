import 'dart:convert';
import '../api/api_client.dart';
import '../config/app_config.dart';
import '../errors/error_handler.dart';
import '../storage/secure_storage.dart';
import '../../features/auth/data/models/auth_dto.dart';
import '../../features/auth/domain/entities/user_entity.dart';

/// Manages authentication state and operations.
/// Communicates with the FastAPI /auth/* endpoints.
class AuthService {
  final ApiClient _apiClient;
  final SecureStorageService _storage;

  AuthService({
    required ApiClient apiClient,
    required SecureStorageService storage,
  })  : _apiClient = apiClient,
        _storage = storage;

  // ─── Authentication Status ────────────────────────────────────────────────

  Future<bool> get isAuthenticated => _storage.hasToken();

  Future<UserEntity?> get currentUser async {
    final userJson = await _storage.getUser();
    if (userJson == null) return null;
    try {
      return UserEntity.fromJson(jsonDecode(userJson) as Map<String, dynamic>);
    } catch (_) {
      return null;
    }
  }

  // ─── Login ────────────────────────────────────────────────────────────────

  Future<UserEntity> login({
    required String email,
    required String password,
  }) async {
    try {
      // Backend uses OAuth2 form-data for login
      final response = await _apiClient.post<Map<String, dynamic>>(
        AppConfig.loginPath,
        data: {'username': email, 'password': password},
        options: _formDataOptions(),
      );

      final dto = TokenResponseDto.fromJson(response.data!);
      await _storage.saveToken(dto.accessToken);

      // Fetch user profile immediately after login
      return _fetchAndCacheUser();
    } catch (e) {
      throw ErrorHandler.handle(e);
    }
  }

  // ─── Register ─────────────────────────────────────────────────────────────

  Future<UserEntity> register({
    required String email,
    required String password,
    required String fullName,
    String archetype = 'Explorer',
    List<String> coreValues = const [],
    List<String> strengths = const [],
    List<String> weaknesses = const [],
  }) async {
    try {
      final response = await _apiClient.post<Map<String, dynamic>>(
        AppConfig.registerPath,
        data: {
          'email': email,
          'password': password,
          'full_name': fullName,
          'archetype': archetype,
          'core_values': coreValues,
          'strengths': strengths,
          'weaknesses': weaknesses,
        },
      );

      final dto = TokenResponseDto.fromJson(response.data!);
      await _storage.saveToken(dto.accessToken);

      return _fetchAndCacheUser();
    } catch (e) {
      throw ErrorHandler.handle(e);
    }
  }

  // ─── Logout ───────────────────────────────────────────────────────────────

  Future<void> logout() async {
    await _storage.clearAll();
  }

  // ─── Private ──────────────────────────────────────────────────────────────

  Future<UserEntity> _fetchAndCacheUser() async {
    final meResponse = await _apiClient.get<Map<String, dynamic>>(
      AppConfig.mePath,
    );
    final user = UserEntity.fromJson(meResponse.data!);
    await _storage.saveUser(jsonEncode(meResponse.data));
    return user;
  }

  dynamic _formDataOptions() {
    // Use form-encoded for OAuth2 password grant
    return null; // Dio handles Map as JSON by default; override Content-Type
  }
}
