import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:life_gps/core/sync/offline_queue.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late SharedPreferences prefs;
  late OfflineQueue queue;

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    prefs = await SharedPreferences.getInstance();
    queue = OfflineQueue(prefs);
  });

  group('OfflineQueue', () {
    test('starts empty', () {
      expect(queue.isEmpty, isTrue);
      expect(queue.getQueue(), isEmpty);
    });

    test('enqueues actions correctly', () async {
      await queue
          .enqueueAction(actionType: 'test_action', payload: {'key': 'val'});
      expect(queue.isEmpty, isFalse);

      final items = queue.getQueue();
      expect(items.length, 1);
      expect(items[0]['type'], 'test_action');
      final payload = items[0]['payload'] as Map<String, dynamic>;
      expect(payload['key'], 'val');
    });

    test('removes items correctly', () async {
      await queue.enqueueAction(actionType: 'action_1', payload: {});
      await queue.enqueueAction(actionType: 'action_2', payload: {});

      expect(queue.getQueue().length, 2);
      await queue.removeAction(0);

      final remaining = queue.getQueue();
      expect(remaining.length, 1);
      expect(remaining[0]['type'], 'action_2');
    });

    test('clears entire queue', () async {
      await queue.enqueueAction(actionType: 'action_1', payload: {});
      await queue.clearQueue();
      expect(queue.isEmpty, isTrue);
    });
  });
}
