import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class OfflineQueue {
  final SharedPreferences _prefs;
  static const String _queueKey = 'life_gps_offline_queue';

  const OfflineQueue(this._prefs);

  Future<void> enqueueAction({
    required String actionType,
    required Map<String, dynamic> payload,
  }) async {
    final list = _prefs.getStringList(_queueKey) ?? [];
    final item = {
      'type': actionType,
      'payload': payload,
      'timestamp': DateTime.now().toIso8601String(),
    };
    list.add(jsonEncode(item));
    await _prefs.setStringList(_queueKey, list);
  }

  List<Map<String, dynamic>> getQueue() {
    final list = _prefs.getStringList(_queueKey) ?? [];
    return list.map((e) => jsonDecode(e) as Map<String, dynamic>).toList();
  }

  Future<void> clearQueue() async {
    await _prefs.remove(_queueKey);
  }

  Future<void> removeAction(int index) async {
    final list = _prefs.getStringList(_queueKey) ?? [];
    if (index >= 0 && index < list.length) {
      list.removeAt(index);
      await _prefs.setStringList(_queueKey, list);
    }
  }

  bool get isEmpty => (_prefs.getStringList(_queueKey) ?? []).isEmpty;
}
