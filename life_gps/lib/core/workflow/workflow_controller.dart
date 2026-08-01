import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../features/behavior/presentation/controllers/behavior_controller.dart';
import '../../features/curator/presentation/controllers/curator_controller.dart';
import '../../features/dashboard/presentation/controllers/dashboard_controller.dart';
import '../../features/identity/presentation/controllers/gap_analysis_controller.dart';
import '../../features/identity/presentation/controllers/identity_controller.dart';
import '../../features/learning/presentation/controllers/learning_loop_controller.dart';
import '../../features/missions/presentation/controllers/mission_controller.dart';
import '../../features/planner/presentation/controllers/planner_controller.dart';
import '../ai/ai_client.dart';
import '../workflow/workflow_event.dart';
import '../workflow/workflow_state.dart';

class WorkflowController extends StateNotifier<WorkflowState> {
  final AiClient _aiClient;
  final Ref? _ref;
  StreamSubscription<WorkflowEvent>? _subscription;

  WorkflowController(this._aiClient, [this._ref]) : super(const WorkflowIdle());

  Future<void> runJudgeMode(String profileName) async {
    state = const WorkflowQueued();
    final res = await _aiClient.workflow.triggerDemoRun(profileName);
    res.fold(
      onSuccess: (data) async {
        await startWorkflow('USER_LOGIN', payload: {'profile_name': profileName});
      },
      onFailure: (failure) {
        state = Failed(workflowId: '', error: 'Demo registration failed: ${failure.message}');
      },
    );
  }

  Future<void> startWorkflow(String eventType,
      {Map<String, dynamic> payload = const {}}) async {
    state = const WorkflowQueued();

    final result = await _aiClient.workflow.triggerWorkflow(
      eventType: eventType,
      payload: payload,
    );

    result.fold(
      onSuccess: (data) {
        final id = data['workflow_id']?.toString() ?? '';
        state = WorkflowRunning(
          workflowId: id,
          progress: 0.0,
          activeAgent: 'Orchestrator',
          logs: const ['Workflow started successfully.'],
          trace: const [],
        );
        _subscribeToStream(id);
      },
      onFailure: (failure) {
        state = Failed(workflowId: '', error: failure.message);
      },
    );
  }

  void _subscribeToStream(String id) {
    _subscription?.cancel();
    _subscription = _aiClient.streaming.streamWorkflowUpdates(id).listen(
      (event) {
        final current = state;
        if (current is! WorkflowRunning) return;

        switch (event) {
          case WorkflowProgress(:final percentage, :final trace):
            state = current.copyWith(
              progress: percentage,
              trace: [...current.trace, ...trace],
            );
          case AgentStarted(:final agentName):
            state = AgentExecuting(
              workflowId: current.workflowId,
              progress: current.progress,
              activeAgent: agentName,
              logs: [...current.logs, 'Agent $agentName started execution.'],
              trace: current.trace,
              agentName: agentName,
            );
          case AgentCompleted(:final agentName):
            state = current.copyWith(
              logs: [...current.logs, 'Agent $agentName finished execution successfully.'],
            );
          case AgentFailed(:final agentName, :final error):
            state = Failed(
              workflowId: current.workflowId,
              error: 'Agent $agentName failed: $error',
            );
            _subscription?.cancel();
          case WorkflowCompleted():
            state = Completed(workflowId: id, result: const {'status': 'finished'});
            _subscription?.cancel();
            _autoRefreshAll();
          case WorkflowCancelled():
            state = Cancelled(workflowId: id);
            _subscription?.cancel();
          case Heartbeat(:final timestamp):
            state = current.copyWith(
              logs: [
                ...current.logs,
                'Keepalive heartbeat received at $timestamp'
              ],
            );
          case WorkflowStarted():
            break;
        }
      },
      onError: (err) {
        state = Failed(workflowId: id, error: 'Stream connection error: $err');
      },
      onDone: () {
        final current = state;
        if (current is WorkflowRunning) {
          state =
              Completed(workflowId: id, result: const {'status': 'finished'});
          _autoRefreshAll();
        }
      },
    );
  }

  void _autoRefreshAll() {
    if (_ref == null) return;
    _ref.invalidate(dashboardControllerProvider);
    _ref.invalidate(missionControllerProvider);
    _ref.invalidate(plannerControllerProvider);
    _ref.invalidate(curatorControllerProvider);
    _ref.invalidate(identityControllerProvider);
    _ref.invalidate(gapAnalysisControllerProvider);
    _ref.invalidate(behaviorControllerProvider);
    _ref.invalidate(learningLoopControllerProvider);
  }

  void cancelWorkflow() {
    final current = state;
    if (current is WorkflowRunning) {
      _subscription?.cancel();
      state = Cancelled(workflowId: current.workflowId);
    }
  }

  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }
}
