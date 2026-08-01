import 'package:flutter_test/flutter_test.dart';
import 'package:life_gps/core/ai/ai_client.dart';
import 'package:life_gps/core/ai/agent_client.dart';
import 'package:life_gps/core/ai/streaming_client.dart';
import 'package:life_gps/core/ai/workflow_client.dart';
import 'package:life_gps/core/utils/result.dart';
import 'package:life_gps/core/workflow/workflow_controller.dart';
import 'package:life_gps/core/workflow/workflow_state.dart';
import 'package:life_gps/core/workflow/workflow_event.dart';

class ManualWorkflowClient implements WorkflowClient {
  Result<Map<String, dynamic>>? nextResult;

  @override
  Future<Result<Map<String, dynamic>>> triggerWorkflow({
    required String eventType,
    Map<String, dynamic> payload = const {},
  }) async {
    return nextResult ?? const Result.failure(NetworkFailure('No result set'));
  }

  @override
  Future<Result<Map<String, dynamic>>> getWorkflowStatus(String id) async {
    return nextResult ?? const Result.failure(NetworkFailure('No result set'));
  }

  @override
  Future<Result<List<dynamic>>> getWorkflowHistory() async {
    return const Result.success([]);
  }

  @override
  Future<Result<Map<String, dynamic>>> triggerDemoRun(String profileName) async {
    return const Result.success({});
  }
}

class ManualStreamingClient implements StreamingClient {
  @override
  Stream<WorkflowEvent> streamWorkflowUpdates(String workflowId) =>
      const Stream.empty();

  @override
  void cancelSubscription() {}

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class ManualAgentClient implements AgentClient {
  @override
  Future<Result<Map<String, dynamic>>> getIdentity() async =>
      const Result.failure(NetworkFailure());

  @override
  Future<Result<Map<String, dynamic>>> updateIdentity(
          Map<String, dynamic> data) async =>
      const Result.failure(NetworkFailure());

  @override
  Future<Result<Map<String, dynamic>>> getBehavior() async =>
      const Result.failure(NetworkFailure());

  @override
  Future<Result<Map<String, dynamic>>> getGapAnalysis() async =>
      const Result.failure(NetworkFailure());

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

void main() {
  late ManualWorkflowClient manualWorkflow;
  late ManualStreamingClient manualStreaming;
  late ManualAgentClient manualAgent;
  late AiClient aiClient;
  late WorkflowController controller;

  setUp(() {
    manualWorkflow = ManualWorkflowClient();
    manualStreaming = ManualStreamingClient();
    manualAgent = ManualAgentClient();

    aiClient = AiClient(
      workflow: manualWorkflow,
      streaming: manualStreaming,
      agent: manualAgent,
    );

    controller = WorkflowController(aiClient);
  });

  group('WorkflowController', () {
    test('initial state is WorkflowIdle', () {
      expect(controller.state, isA<WorkflowIdle>());
    });

    test('failure to trigger workflow transitions state to Failed', () async {
      manualWorkflow.nextResult =
          const Result.failure(NetworkFailure('Server down'));

      await controller.startWorkflow('USER_ONBOARDED');

      expect(controller.state, isA<Failed>());
      expect((controller.state as Failed).error, contains('Server down'));
    });
  });
}
