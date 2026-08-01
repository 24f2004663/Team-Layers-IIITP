import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

/// Handles caching of API JSON responses with a TTL.
class CacheService {
  final SharedPreferences _prefs;

  const CacheService(this._prefs);

  static const String _cachePrefix = 'life_gps_cache_';
  static const String _expiryPrefix = 'life_gps_expiry_';

  Future<void> cacheData(
      String key, Map<String, dynamic> data, Duration ttl) async {
    final cacheKey = '$_cachePrefix$key';
    final expiryKey = '$_expiryPrefix$key';
    final expiryTime = DateTime.now().add(ttl).millisecondsSinceEpoch;

    await _prefs.setString(cacheKey, jsonEncode(data));
    await _prefs.setInt(expiryKey, expiryTime);
  }

  Future<void> cacheListData(
      String key, List<dynamic> data, Duration ttl) async {
    final cacheKey = '$_cachePrefix$key';
    final expiryKey = '$_expiryPrefix$key';
    final expiryTime = DateTime.now().add(ttl).millisecondsSinceEpoch;

    await _prefs.setString(cacheKey, jsonEncode(data));
    await _prefs.setInt(expiryKey, expiryTime);
  }

  String? getCachedString(String key) {
    final cacheKey = '$_cachePrefix$key';
    final expiryKey = '$_expiryPrefix$key';

    final expiryTime = _prefs.getInt(expiryKey);
    if (expiryTime == null ||
        DateTime.now().millisecondsSinceEpoch > expiryTime) {
      // Expired or not cached
      invalidateCache(key);
      return null;
    }
    return _prefs.getString(cacheKey);
  }

  Map<String, dynamic>? getCachedData(String key) {
    final cached = getCachedString(key);
    if (cached == null) return null;
    try {
      return jsonDecode(cached) as Map<String, dynamic>;
    } catch (_) {
      return null;
    }
  }

  List<dynamic>? getCachedListData(String key) {
    final cached = getCachedString(key);
    if (cached == null) return null;
    try {
      return jsonDecode(cached) as List<dynamic>;
    } catch (_) {
      return null;
    }
  }

  Future<void> invalidateCache(String key) async {
    await _prefs.remove('$_cachePrefix$key');
    await _prefs.remove('$_expiryPrefix$key');
  }

  Future<void> clearAllCache() async {
    final keys = _prefs.getKeys();
    for (final key in keys) {
      if (key.startsWith(_cachePrefix) || key.startsWith(_expiryPrefix)) {
        await _prefs.remove(key);
      }
    }
  }
}
