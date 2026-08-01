import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';

/// Wraps flutter_secure_storage with typed Life-GPS key operations.
class SecureStorageService {
  final FlutterSecureStorage _storage;

  SecureStorageService()
      : _storage = const FlutterSecureStorage(
          aOptions: AndroidOptions(encryptedSharedPreferences: true),
          iOptions: IOSOptions(
            accessibility: KeychainAccessibility.first_unlock_this_device,
          ),
        );

  // ─── Token ────────────────────────────────────────────────────────────────

  Future<void> saveToken(String token) =>
      _storage.write(key: AppConstants.tokenKey, value: token);

  Future<String?> getToken() => _storage.read(key: AppConstants.tokenKey);

  Future<void> deleteToken() => _storage.delete(key: AppConstants.tokenKey);

  Future<bool> hasToken() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  // ─── User ─────────────────────────────────────────────────────────────────

  Future<void> saveUser(String userJson) =>
      _storage.write(key: AppConstants.userKey, value: userJson);

  Future<String?> getUser() => _storage.read(key: AppConstants.userKey);

  Future<void> deleteUser() => _storage.delete(key: AppConstants.userKey);

  // ─── Onboarding ──────────────────────────────────────────────────────────

  Future<void> setOnboardingComplete() =>
      _storage.write(key: AppConstants.onboardingKey, value: 'true');

  Future<bool> isOnboardingComplete() async {
    final val = await _storage.read(key: AppConstants.onboardingKey);
    return val == 'true';
  }

  // ─── Clear All ───────────────────────────────────────────────────────────

  Future<void> clearAll() => _storage.deleteAll();
}
