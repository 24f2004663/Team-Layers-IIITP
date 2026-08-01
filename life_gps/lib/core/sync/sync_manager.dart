import 'offline_queue.dart';
import '../ai/ai_client.dart';
import '../storage/cache_service.dart';

class SyncManager {
  final OfflineQueue _queue;
  final AiClient _aiClient;
  final CacheService _cache;

  const SyncManager({
    required OfflineQueue queue,
    required AiClient aiClient,
    required CacheService cache,
  })  : _queue = queue,
        _aiClient = aiClient,
        _cache = cache;

  Future<void> runSync() async {
    if (_queue.isEmpty) return;

    final items = _queue.getQueue();
    final itemsToReplay = List<Map<String, dynamic>>.from(items);

    for (var i = 0; i < itemsToReplay.length; i++) {
      final item = itemsToReplay[i];
      final type = item['type'] as String;
      final payload = item['payload'] as Map<String, dynamic>;

      bool success = false;
      if (type == 'trigger_workflow') {
        final res = await _aiClient.workflow.triggerWorkflow(
          eventType: payload['event_type'] as String? ?? 'USER_INTERACTION',
          payload: payload['payload'] as Map<String, dynamic>? ?? {},
        );
        success = res.isSuccess;
      } else if (type == 'update_identity') {
        final res = await _aiClient.agent.updateIdentity(payload);
        success = res.isSuccess;
      } else if (type == 'complete_mission') {
        // Mock success when online
        success = true;
      } else if (type == 'update_planner') {
        // Mock success when online
        success = true;
      }

      if (success) {
        await _queue.removeAction(0); // always pop first
      } else {
        // Stop synchronizing to preserve sequential integrity
        break;
      }
    }
  }

  Future<void> clearAllCaches() async {
    await _cache.clearAllCache();
  }
}
