import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../config/app_config.dart';
import '../storage/secure_storage.dart';

/// Payload received on each WebSocket tick.
class WorkflowUpdate {
  final String workflowId;
  final String status;
  final String currentAgent;
  final List<String> completedAgents;
  final List<String> failedAgents;
  final double completionPercentage;
  final List<String> decisionTrace;
  final List<String> errors;

  const WorkflowUpdate({
    required this.workflowId,
    required this.status,
    required this.currentAgent,
    required this.completedAgents,
    required this.failedAgents,
    required this.completionPercentage,
    required this.decisionTrace,
    required this.errors,
  });

  factory WorkflowUpdate.fromJson(Map<String, dynamic> json) => WorkflowUpdate(
        workflowId: json['workflow_id'] as String? ?? '',
        status: json['status'] as String? ?? 'pending',
        currentAgent: json['current_agent'] as String? ?? '',
        completedAgents: List<String>.from(json['completed_agents'] ?? []),
        failedAgents: List<String>.from(json['failed_agents'] ?? []),
        completionPercentage:
            (json['completion_percentage'] as num?)?.toDouble() ?? 0.0,
        decisionTrace: List<String>.from(json['decision_trace'] ?? []),
        errors: List<String>.from(json['errors'] ?? []),
      );
}

/// Manages a single WebSocket connection to the Life-GPS workflow stream.
/// Supports reconnection with exponential backoff.
class WebSocketService {
  final SecureStorageService _storage;

  WebSocketChannel? _channel;
  StreamController<WorkflowUpdate>? _controller;
  String? _activeWorkflowId;
  int _reconnectAttempts = 0;
  bool _disposed = false;

  WebSocketService({required SecureStorageService storage})
      : _storage = storage;

  // ─── Public ───────────────────────────────────────────────────────────────

  /// Subscribes to updates for [workflowId].
  /// Returns a stream of [WorkflowUpdate] objects.
  Stream<WorkflowUpdate> subscribe(String workflowId) {
    _activeWorkflowId = workflowId;
    _reconnectAttempts = 0;
    _disposed = false;
    _controller?.close();
    _controller = StreamController<WorkflowUpdate>.broadcast();
    _connect();
    return _controller!.stream;
  }

  void dispose() {
    _disposed = true;
    _channel?.sink.close();
    _controller?.close();
  }

  // ─── Private ──────────────────────────────────────────────────────────────

  void _connect() async {
    if (_disposed) return;
    try {
      final hasToken = await _storage.hasToken();
      if (!hasToken) {
        // No stored token found; proceeding as anonymous socket channel connection
      }
      final uri = Uri.parse(AppConfig.wsWorkflowEndpoint);
      _channel = WebSocketChannel.connect(uri);

      // Send subscription message with workflow_id
      _channel!.sink.add(jsonEncode({'workflow_id': _activeWorkflowId}));

      _channel!.stream.listen(
        (data) {
          _reconnectAttempts = 0; // reset on successful message
          try {
            final json = jsonDecode(data as String) as Map<String, dynamic>;
            if (json.containsKey('error')) return;
            final update = WorkflowUpdate.fromJson(json);
            _controller?.add(update);
            if (update.status == 'completed' || update.status == 'failed') {
              _controller?.close();
            }
          } catch (_) {}
        },
        onError: (_) => _scheduleReconnect(),
        onDone: () => _scheduleReconnect(),
        cancelOnError: false,
      );
    } catch (_) {
      _scheduleReconnect();
    }
  }

  void _scheduleReconnect() {
    if (_disposed) return;
    if (_reconnectAttempts >= AppConfig.wsMaxReconnectAttempts) {
      _controller
          ?.addError(Exception('WebSocket max reconnect attempts reached.'));
      _controller?.close();
      return;
    }
    final delay = AppConfig.wsReconnectBaseDelay * (1 << _reconnectAttempts);
    _reconnectAttempts++;
    Future.delayed(delay, _connect);
  }
}
