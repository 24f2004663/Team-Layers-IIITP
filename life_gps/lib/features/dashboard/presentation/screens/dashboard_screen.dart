import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/router/app_router.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/widgets/loading_widget.dart';
import '../../../../core/widgets/error_banner.dart';
import '../../../../core/widgets/error_state_widget.dart';
import '../../../workflow/presentation/widgets/workflow_visualization_widget.dart';
import '../../../../core/di/providers.dart';
import '../controllers/dashboard_controller.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(dashboardControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            const ErrorBanner(),
            Expanded(
              child: state.when(
                loading: () => const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: LoadingWidget(itemCount: 4, itemHeight: 120),
                ),
                error: (err, stack) => ErrorStateWidget(
                  message: err.toString(),
                  onRetry: () => ref
                      .read(dashboardControllerProvider.notifier)
                      .refreshData(),
                ),
                data: (data) {
                  final summary = data.summary;
                  final today = data.today;
                  final progress = data.progress;
                  final future = data.future;

                  return RefreshIndicator(
                    onRefresh: () => ref
                        .read(dashboardControllerProvider.notifier)
                        .refreshData(),
                    child: SingleChildScrollView(
                      physics: const AlwaysScrollableScrollPhysics(),
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // Top Greeting & Archetype Row
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Good Morning,',
                                    style: tt.bodyLarge
                                        ?.copyWith(color: cs.onSurfaceVariant),
                                  ),
                                  Text(
                                    'User',
                                    style: tt.headlineMedium
                                        ?.copyWith(fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                              GestureDetector(
                                onTap: () => context.go(AppRoutes.profile),
                                child: Hero(
                                  tag: 'archetype_profile_badge',
                                  child: Material(
                                    color: Colors.transparent,
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 16, vertical: 8),
                                      decoration: BoxDecoration(
                                        gradient: LinearGradient(
                                          colors: [cs.primary, cs.secondary],
                                        ),
                                        borderRadius: BorderRadius.circular(20),
                                      ),
                                      child: Text(
                                        summary.archetype,
                                        style: tt.labelLarge?.copyWith(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 24),

                          // Core Stats Glassmorphic Panel
                          GlassmorphicDecorator.wrap(
                            context: context,
                            color: cs.primary,
                            child: Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Row(
                                children: [
                                  _StatWidget(
                                    title: 'Growth Index',
                                    value: summary.compositeGrowthIndex
                                        .toStringAsFixed(1),
                                    icon: Icons.trending_up_rounded,
                                    color: cs.primary,
                                  ),
                                  _VerticalDivider(),
                                  _StatWidget(
                                    title: 'Active Goals',
                                    value: summary.activeGoalsCount.toString(),
                                    icon: Icons.flag_rounded,
                                    color: cs.secondary,
                                  ),
                                  _VerticalDivider(),
                                  _StatWidget(
                                    title: 'Focus Rating',
                                    value:
                                        '${progress.consistencyDelta.toInt()}%',
                                    icon: Icons.track_changes_rounded,
                                    color: cs.tertiary,
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(height: 20),

                          // Today's Mission & Progress Indicator
                          Text(
                            "Today's Highlight",
                            style: tt.titleMedium
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 12),
                          GlassmorphicDecorator.wrap(
                            context: context,
                            color: cs.surfaceContainerHighest,
                            child: Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Row(
                                children: [
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'CURRENT MISSION',
                                          style: tt.labelSmall?.copyWith(
                                            color: cs.primary,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          today.currentMission ??
                                              'No active mission target',
                                          style: tt.titleLarge?.copyWith(
                                              fontWeight: FontWeight.bold),
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          'Focus: ${today.totalFocusedMinutes}m  •  Breaks: ${today.breaksCount}',
                                          style: tt.bodySmall?.copyWith(
                                              color: cs.onSurfaceVariant),
                                        ),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(width: 16),
                                  Stack(
                                    alignment: Alignment.center,
                                    children: [
                                      SizedBox(
                                        width: 64,
                                        height: 64,
                                        child: CircularProgressIndicator(
                                          value: progress.completionRate / 100,
                                          strokeWidth: 6,
                                          backgroundColor:
                                              cs.outline.withOpacity(0.15),
                                          color: cs.tertiary,
                                        ),
                                      ),
                                      Text(
                                        '${progress.completionRate.toInt()}%',
                                        style: tt.bodySmall?.copyWith(
                                            fontWeight: FontWeight.bold),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ),
                          const SizedBox(height: 20),

                          // Current Routine & Energy Prediction
                          Text(
                            'Energy & Routine Schedule',
                            style: tt.titleMedium
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 12),
                          GlassmorphicDecorator.wrap(
                            context: context,
                            color: cs.surfaceContainerHighest,
                            child: Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Column(
                                children:
                                    progress.energyLevels.entries.map((entry) {
                                  return Padding(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 8.0),
                                    child: Row(
                                      children: [
                                        SizedBox(
                                          width: 80,
                                          child: Text(
                                            entry.key,
                                            style: tt.bodyMedium?.copyWith(
                                                fontWeight: FontWeight.bold),
                                          ),
                                        ),
                                        Expanded(
                                          child: ClipRRect(
                                            borderRadius:
                                                BorderRadius.circular(4),
                                            child: LinearProgressIndicator(
                                              value: entry.value,
                                              backgroundColor:
                                                  cs.outline.withOpacity(0.15),
                                              color: entry.value > 0.7
                                                  ? cs.primary
                                                  : cs.secondary,
                                              minHeight: 6,
                                            ),
                                          ),
                                        ),
                                        const SizedBox(width: 12),
                                        Text(
                                          '${(entry.value * 100).toInt()}%',
                                          style: tt.bodySmall?.copyWith(
                                              fontWeight: FontWeight.bold),
                                        ),
                                      ],
                                    ),
                                  );
                                }).toList(),
                              ),
                            ),
                          ),
                          const SizedBox(height: 20),

                          // Signature Live Workflow Visualizer
                          Text(
                            'AI Orchestrator Stream',
                            style: tt.titleMedium
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 12),
                          const WorkflowVisualizationWidget(),
                          const SizedBox(height: 20),

                          // Learning bundle Recommendations
                          Text(
                            'Recommended Path Intervention',
                            style: tt.titleMedium
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 12),
                          ListView.separated(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            itemCount: future.recommendedInterventions.length,
                            separatorBuilder: (context, index) =>
                                const SizedBox(height: 10),
                            itemBuilder: (context, index) {
                              final item =
                                  future.recommendedInterventions[index];
                              return GlassmorphicDecorator.wrap(
                                context: context,
                                color: cs.surfaceContainerHighest,
                                child: ListTile(
                                  leading: CircleAvatar(
                                    backgroundColor:
                                        cs.primary.withOpacity(0.1),
                                    child: Icon(Icons.school_rounded,
                                        color: cs.primary),
                                  ),
                                  title: Text(
                                    item,
                                    style: tt.bodyMedium
                                        ?.copyWith(fontWeight: FontWeight.bold),
                                  ),
                                  subtitle: Text(
                                    'AI Confidence Rating: ${(future.calibrationFactor * 100).toStringAsFixed(1)}%',
                                    style: tt.bodySmall
                                        ?.copyWith(color: cs.onSurfaceVariant),
                                  ),
                                  trailing: Icon(Icons.chevron_right_rounded,
                                      color: cs.primary),
                                  onTap: () => context.go(AppRoutes.curator),
                                ),
                              );
                            },
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        key: const ValueKey('judge_mode_button'),
        onPressed: () => _showJudgeModeBottomSheet(context, ref),
        label: const Text('Run AI Demo'),
        icon: const Icon(Icons.play_arrow_rounded),
      ),
    );
  }

  void _showJudgeModeBottomSheet(BuildContext context, WidgetRef ref) {
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) {
        return GlassmorphicDecorator.wrap(
          context: context,
          borderRadius: 24,
          color: cs.surface,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Judge Mode: Run AI Demo',
                  style: tt.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'Select a profile scenario to execute the E2E Agentic Operating System workflow.',
                  style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                ...['Student', 'Software Engineer', 'Founder', 'Career Switcher'].map((profile) {
                  IconData icon;
                  String desc;
                  switch (profile) {
                    case 'Student':
                      icon = Icons.school_rounded;
                      desc = 'Focus: Basic Python variables & syntax learning loops';
                      break;
                    case 'Software Engineer':
                      icon = Icons.code_rounded;
                      desc = 'Focus: Mastering advanced data structures & idioms';
                      break;
                    case 'Founder':
                      icon = Icons.business_center_rounded;
                      desc = 'Focus: Rapid agile planning & sprint cycles';
                      break;
                    case 'Career Switcher':
                    default:
                      icon = Icons.transform_rounded;
                      desc = 'Focus: Mapped capability gap transitions';
                      break;
                  }

                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12.0),
                    child: InkWell(
                      onTap: () {
                        Navigator.pop(context);
                        ref.read(workflowControllerProvider.notifier).runJudgeMode(profile);
                        _showLiveWorkflowProgressOverlay(context);
                      },
                      borderRadius: BorderRadius.circular(16),
                      child: Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          border: Border.all(color: cs.outline.withOpacity(0.15)),
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Row(
                          children: [
                            CircleAvatar(
                              backgroundColor: cs.primary.withOpacity(0.1),
                              child: Icon(icon, color: cs.primary),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(profile, style: tt.bodyLarge?.copyWith(fontWeight: FontWeight.bold)),
                                  Text(desc, style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
                                ],
                              ),
                            ),
                            Icon(Icons.play_arrow_rounded, color: cs.primary),
                          ],
                        ),
                      ),
                    ),
                  );
                }),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showLiveWorkflowProgressOverlay(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    showModalBottomSheet(
      context: context,
      isDismissible: true,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) {
        return DraggableScrollableSheet(
          initialChildSize: 0.85,
          minChildSize: 0.5,
          maxChildSize: 0.95,
          builder: (context, scrollController) {
            return GlassmorphicDecorator.wrap(
              context: context,
              borderRadius: 24,
              color: cs.surface,
              child: SingleChildScrollView(
                controller: scrollController,
                padding: const EdgeInsets.all(20),
                child: const Column(
                  children: [
                    SizedBox(height: 10),
                    WorkflowVisualizationWidget(),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }
}

class _StatWidget extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _StatWidget({
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    final tt = Theme.of(context).textTheme;
    return Expanded(
      child: Column(
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 6),
          Text(
            value,
            style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 2),
          Text(
            title,
            style: tt.bodySmall?.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

class _VerticalDivider extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 36,
      width: 1,
      color: Theme.of(context).colorScheme.outline.withOpacity(0.2),
    );
  }
}
