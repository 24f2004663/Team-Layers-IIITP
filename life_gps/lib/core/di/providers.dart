import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../api/api_client.dart';
import '../api/interceptors/auth_interceptor.dart';
import '../services/auth_service.dart';
import '../services/websocket_service.dart';
import '../storage/secure_storage.dart';
import '../storage/cache_service.dart';
import '../ai/ai_client.dart';
import '../ai/workflow_client.dart';
import '../ai/streaming_client.dart';
import '../ai/agent_client.dart';
import '../workflow/workflow_controller.dart';
import '../workflow/workflow_state.dart';
import '../sync/offline_queue.dart';
import '../sync/sync_manager.dart';

// ─── Storage ─────────────────────────────────────────────────────────────────

final secureStorageProvider = Provider<SecureStorageService>(
  (_) => SecureStorageService(),
  name: 'secureStorageProvider',
);

final sharedPreferencesProvider = Provider<SharedPreferences>((_) {
  throw UnimplementedError('Initialize in main first');
});

final cacheServiceProvider = Provider<CacheService>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return CacheService(prefs);
});

// ─── API ─────────────────────────────────────────────────────────────────────

final authInterceptorProvider = Provider<AuthInterceptor>((ref) {
  final storage = ref.read(secureStorageProvider);
  return AuthInterceptor(storage: storage);
}, name: 'authInterceptorProvider');

final apiClientProvider = Provider<ApiClient>((ref) {
  final authInterceptor = ref.read(authInterceptorProvider);
  return ApiClient(authInterceptor: authInterceptor);
}, name: 'apiClientProvider');

// ─── Services ─────────────────────────────────────────────────────────────────

final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService(
    apiClient: ref.read(apiClientProvider),
    storage: ref.read(secureStorageProvider),
  );
}, name: 'authServiceProvider');

final webSocketServiceProvider = Provider<WebSocketService>((ref) {
  return WebSocketService(storage: ref.read(secureStorageProvider));
}, name: 'webSocketServiceProvider');

// ─── Auth State ───────────────────────────────────────────────────────────────

/// Async auth state — true if a JWT token exists in secure storage.
final authStateProvider = FutureProvider<bool>((ref) async {
  final storage = ref.read(secureStorageProvider);
  return storage.hasToken();
}, name: 'authStateProvider');

// ─── AI Clients ───────────────────────────────────────────────────────────────

final workflowClientProvider = Provider<WorkflowClient>((ref) {
  return WorkflowClient(ref.watch(apiClientProvider));
});

final streamingClientProvider = Provider<StreamingClient>((ref) {
  return StreamingClient(ref.watch(webSocketServiceProvider));
});

final agentClientProvider = Provider<AgentClient>((ref) {
  return AgentClient(ref.watch(apiClientProvider));
});

final aiClientProvider = Provider<AiClient>((ref) {
  return AiClient(
    workflow: ref.watch(workflowClientProvider),
    streaming: ref.watch(streamingClientProvider),
    agent: ref.watch(agentClientProvider),
  );
});

// ─── Workflow controller ──────────────────────────────────────────────────────

final workflowControllerProvider =
    StateNotifierProvider<WorkflowController, WorkflowState>((ref) {
  return WorkflowController(ref.watch(aiClientProvider), ref);
});

// ─── Sync & Offline Queue ─────────────────────────────────────────────────────

final offlineQueueProvider = Provider<OfflineQueue>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return OfflineQueue(prefs);
});

final syncManagerProvider = Provider<SyncManager>((ref) {
  return SyncManager(
    queue: ref.watch(offlineQueueProvider),
    aiClient: ref.watch(aiClientProvider),
    cache: ref.watch(cacheServiceProvider),
  );
});

// ─── Theme ────────────────────────────────────────────────────────────────────

final themeModeProvider = StateProvider<bool>(
  (_) => true, // true = dark mode
  name: 'themeModeProvider',
);
