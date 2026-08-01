import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/di/providers.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/workflow/workflow_state.dart';

class WorkflowVisualizationWidget extends ConsumerStatefulWidget {
  const WorkflowVisualizationWidget({super.key});

  @override
  ConsumerState<WorkflowVisualizationWidget> createState() =>
      _WorkflowVisualizationWidgetState();
}

class _WorkflowVisualizationWidgetState
    extends ConsumerState<WorkflowVisualizationWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  final ScrollController _terminalScrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _terminalScrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    if (_terminalScrollController.hasClients) {
      _terminalScrollController.animateTo(
        _terminalScrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(workflowControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    if (state is WorkflowIdle) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.bolt_rounded, size: 48, color: cs.primary.withOpacity(0.5)),
              const SizedBox(height: 12),
              Text(
                'Workflow Engine Idle',
                style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(
                'Perform an action to trigger the AI Orchestrator',
                style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      );
    }

    final String workflowId = _getWorkflowId(state);
    final double progress = _getProgress(state);
    final String activeAgent = _getActiveAgent(state);
    final List<String> logs = _getLogs(state);

    // Auto-scroll logs when they change
    WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());

    // Define 8 stages
    final stages = [
      const _StageInfo('Identity', 'IdentityAgent', 'Evaluates user archetype and values', Icons.fingerprint_rounded),
      const _StageInfo('Behavior', 'BehaviorAgent', 'Predicts routines and energy levels', Icons.psychology_rounded),
      const _StageInfo('Gap Analysis', 'GapAnalysisAgent', 'Identifies performance discrepancies', Icons.analytics_rounded),
      const _StageInfo('Decision Engine', 'DecisionEngine', 'Weighs priority and action tracks', Icons.insights_rounded),
      const _StageInfo('Mission Engine', 'MissionEngine', 'Generates milestone target cards', Icons.rocket_launch_rounded),
      const _StageInfo('Planner', 'PlannerAgent', 'Optimizes schedule timeline blocks', Icons.calendar_today_rounded),
      const _StageInfo('Curator', 'CuratorAgent', 'Ranks supporting learning bundles', Icons.auto_stories_rounded),
      const _StageInfo('Learning Loop', 'LearningLoopAgent', 'Aggregates progress analytics', Icons.loop_rounded),
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Header Status Card
        GlassmorphicDecorator.wrap(
          context: context,
          color: cs.primary,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            key: const ValueKey('workflow_header_container'),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'AI Operating System Run',
                      style: tt.titleSmall?.copyWith(fontWeight: FontWeight.bold, color: cs.primary),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: _getStatusColor(state, cs).withOpacity(0.15),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        _getStatusText(state).toUpperCase(),
                        style: tt.labelSmall?.copyWith(
                          color: _getStatusColor(state, cs),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  'ID: $workflowId',
                  style: tt.bodySmall?.copyWith(fontFamily: 'monospace', color: cs.onSurfaceVariant),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(4),
                        child: LinearProgressIndicator(
                          value: progress / 100,
                          backgroundColor: cs.outline.withOpacity(0.2),
                          color: cs.primary,
                          minHeight: 8,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Text(
                      '${progress.toInt()}%',
                      style: tt.bodyMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  'Estimated time remaining: ${_getRemainingTime(progress)}',
                  style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 20),

        // Stages List
        ListView.separated(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: stages.length,
          separatorBuilder: (context, index) {
            // Render glowing animated connectors between cards
            final nextStage = stages[index + 1];
            final nextStatus = _getStageStatus(nextStage.agentName, activeAgent, state, logs);
            final currentStage = stages[index];
            final currentStatus = _getStageStatus(currentStage.agentName, activeAgent, state, logs);

            final isActive = (currentStatus == _StageStatus.completed && nextStatus == _StageStatus.running) ||
                (currentStatus == _StageStatus.completed && nextStatus == _StageStatus.completed);

            return Container(
              margin: const EdgeInsets.only(left: 32),
              height: 20,
              width: 2,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: isActive
                      ? [cs.tertiary, cs.primary]
                      : [cs.outline.withOpacity(0.15), cs.outline.withOpacity(0.15)],
                ),
              ),
            );
          },
          itemBuilder: (context, index) {
            final stage = stages[index];
            final status = _getStageStatus(stage.agentName, activeAgent, state, logs);
            final isCompleted = status == _StageStatus.completed;
            final isRunning = status == _StageStatus.running;
            final isFailed = status == _StageStatus.failed;

            Color statusColor;
            IconData statusIcon;

            switch (status) {
              case _StageStatus.completed:
                statusColor = cs.tertiary;
                statusIcon = Icons.check_circle_rounded;
                break;
              case _StageStatus.running:
                statusColor = cs.primary;
                statusIcon = Icons.run_circle_rounded;
                break;
              case _StageStatus.failed:
                statusColor = cs.error;
                statusIcon = Icons.error_rounded;
                break;
              case _StageStatus.waiting:
              default:
                statusColor = cs.outline;
                statusIcon = Icons.radio_button_unchecked_rounded;
                break;
            }

            return AnimatedBuilder(
              animation: _pulseController,
              builder: (context, child) {
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 350),
                  decoration: isRunning
                      ? BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: cs.primary.withOpacity(0.15 * _pulseController.value),
                              blurRadius: 12,
                              spreadRadius: 2,
                            ),
                          ],
                        )
                      : null,
                  child: GlassmorphicDecorator.wrap(
                    context: context,
                    color: isRunning ? cs.primary : cs.surface,
                    borderOpacity: isRunning ? 0.4 : 0.15,
                    child: Theme(
                      data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
                      child: ExpansionTile(
                        key: ValueKey('stage_${stage.title}_tile'),
                        leading: CircleAvatar(
                          backgroundColor: statusColor.withOpacity(0.1),
                          child: Icon(stage.icon, color: statusColor, size: 20),
                        ),
                        title: Text(
                          stage.title,
                          style: tt.bodyLarge?.copyWith(
                            fontWeight: isRunning ? FontWeight.bold : FontWeight.w600,
                            color: isRunning ? cs.primary : null,
                          ),
                        ),
                        subtitle: Text(
                          stage.description,
                          style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                        ),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(statusIcon, color: statusColor, size: 18),
                            const SizedBox(width: 6),
                            Text(
                              isRunning
                                  ? 'RUNNING'
                                  : isCompleted
                                      ? 'COMPLETED'
                                      : isFailed
                                          ? 'FAILED'
                                          : 'PENDING',
                              style: tt.labelSmall?.copyWith(
                                color: statusColor,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(left: 16.0, right: 16.0, bottom: 12.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                const Divider(height: 16),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text('Latency Prediction', style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
                                    Text(
                                      isCompleted || isRunning ? '0.45s' : '0.00s',
                                      style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text('AI Confidence Level', style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
                                    Text(
                                      isCompleted ? '96.4%' : isRunning ? 'Calculating...' : '0.0%',
                                      style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),
                                Text(
                                  'Decision Trace Insights',
                                  style: tt.labelMedium?.copyWith(fontWeight: FontWeight.bold, color: cs.primary),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  isCompleted
                                      ? 'Target parameters evaluated successfully with weights stored into local database registry.'
                                      : isRunning
                                          ? 'Executing internal agent engine steps, matching active user heuristic variables...'
                                          : 'Waiting for upstream pipeline triggers.',
                                  style: tt.bodySmall,
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            );
          },
        ),
        const SizedBox(height: 24),

        // Monospaced Live Log Terminal Console
        Text(
          'Orchestrator Terminal Stream',
          style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        Container(
          height: 160,
          decoration: BoxDecoration(
            color: Colors.black.withOpacity(0.95),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: cs.outline.withOpacity(0.3)),
          ),
          padding: const EdgeInsets.all(12),
          child: logs.isEmpty
              ? Center(
                  child: Text(
                    '[SYSTEM] Idle - awaiting websocket sequence...',
                    style: tt.bodySmall?.copyWith(
                      color: Colors.greenAccent,
                      fontFamily: 'monospace',
                    ),
                  ),
                )
              : Scrollbar(
                  controller: _terminalScrollController,
                  child: ListView.builder(
                    controller: _terminalScrollController,
                    itemCount: logs.length,
                    itemBuilder: (context, index) {
                      final logLine = logs[index];
                      Color logColor = Colors.white70;

                      if (logLine.contains('Initiating') || logLine.contains('Triggered')) {
                        logColor = cs.primary;
                      } else if (logLine.contains('finished') || logLine.contains('Successfully')) {
                        logColor = Colors.greenAccent;
                      } else if (logLine.contains('error') || logLine.contains('failed')) {
                        logColor = Colors.redAccent;
                      }

                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 2.0),
                        child: Text(
                          logLine,
                          style: tt.bodySmall?.copyWith(
                            color: logColor,
                            fontFamily: 'monospace',
                            fontSize: 11,
                          ),
                        ),
                      );
                    },
                  ),
                ),
        ),
      ],
    );
  }

  // Helper getters
  String _getWorkflowId(WorkflowState state) {
    if (state is WorkflowRunning) return state.workflowId;
    if (state is Completed) return state.workflowId;
    if (state is Failed) return state.workflowId;
    if (state is Cancelled) return state.workflowId;
    return 'none';
  }

  double _getProgress(WorkflowState state) {
    if (state is WorkflowRunning) return state.progress;
    if (state is Completed) return 100.0;
    return 0.0;
  }

  String _getActiveAgent(WorkflowState state) {
    if (state is WorkflowRunning) return state.activeAgent;
    return '';
  }

  List<String> _getLogs(WorkflowState state) {
    if (state is WorkflowRunning) return state.logs;
    return [];
  }

  String _getStatusText(WorkflowState state) {
    if (state is WorkflowQueued) return 'Queued';
    if (state is AgentExecuting) return 'Executing';
    if (state is WaitingForUser) return 'Waiting for user input';
    if (state is WorkflowRunning) return 'Running';
    if (state is Completed) return 'Completed';
    if (state is Failed) return 'Failed';
    if (state is Cancelled) return 'Cancelled';
    return 'Idle';
  }

  Color _getStatusColor(WorkflowState state, ColorScheme cs) {
    if (state is Completed) return cs.tertiary;
    if (state is Failed) return cs.error;
    if (state is Cancelled) return cs.outline;
    return cs.primary;
  }

  String _getRemainingTime(double progress) {
    if (progress >= 100) return '0s';
    final remaining = ((100 - progress) * 0.15).toInt();
    return '${remaining}s';
  }

  _StageStatus _getStageStatus(
      String agentName, String activeAgent, WorkflowState state, List<String> logs) {
    if (state is Completed) return _StageStatus.completed;
    if (state is Failed && activeAgent == agentName) return _StageStatus.failed;

    // Check logs/trace for completed stages
    final wasCompleted = logs.any((log) => log.contains('finished') && log.contains(agentName)) ||
        logs.any((log) => log.contains('Successfully registered') && log.contains(agentName));

    if (wasCompleted) return _StageStatus.completed;
    if (activeAgent == agentName) return _StageStatus.running;

    return _StageStatus.waiting;
  }
}

class _StageInfo {
  final String title;
  final String agentName;
  final String description;
  final IconData icon;

  const _StageInfo(this.title, this.agentName, this.description, this.icon);
}

enum _StageStatus {
  waiting,
  running,
  completed,
  failed,
}
