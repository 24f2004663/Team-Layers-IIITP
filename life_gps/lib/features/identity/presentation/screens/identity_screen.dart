import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/widgets/error_state_widget.dart';
import '../../../../core/widgets/loading_widget.dart';
import '../controllers/identity_controller.dart';
import '../controllers/gap_analysis_controller.dart';

class IdentityScreen extends ConsumerWidget {
  const IdentityScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final identityState = ref.watch(identityControllerProvider);
    final gapState = ref.watch(gapAnalysisControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Identity & Archetype'),
        actions: [
          IconButton(
            key: const ValueKey('identity_refresh_button'),
            icon: const Icon(Icons.refresh_rounded),
            onPressed: () {
              ref.read(identityControllerProvider.notifier).refreshData();
              ref.read(gapAnalysisControllerProvider.notifier).refreshData();
            },
          ),
        ],
      ),
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async {
            ref.read(identityControllerProvider.notifier).refreshData();
            ref.read(gapAnalysisControllerProvider.notifier).refreshData();
          },
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Identity Loading/Error states
                identityState.when(
                  loading: () => const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: LoadingWidget(itemCount: 3, itemHeight: 140),
                  ),
                  error: (err, stack) => ErrorStateWidget(
                    message: err.toString(),
                    onRetry: () => ref
                        .read(identityControllerProvider.notifier)
                        .refreshData(),
                  ),
                  data: (identity) {
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Core Archetype Card
                        GlassmorphicDecorator.wrap(
                          context: context,
                          color: cs.primary,
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'CURRENT IDENTITY ARCHETYPE',
                                  style: tt.labelSmall?.copyWith(
                                    color: cs.primary,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 6),
                                Hero(
                                  tag: 'archetype_profile_badge',
                                  child: Material(
                                    color: Colors.transparent,
                                    child: Text(
                                      identity.archetype,
                                      style: tt.headlineMedium?.copyWith(
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  'Target: AI Software Architect',
                                  style: tt.bodyLarge?.copyWith(
                                    fontWeight: FontWeight.w500,
                                    color: cs.onSurfaceVariant,
                                  ),
                                ),
                                const Divider(height: 24),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      'Confidence Index:',
                                      style: tt.bodySmall?.copyWith(
                                        color: cs.onSurfaceVariant,
                                      ),
                                    ),
                                    Text(
                                      '85%',
                                      style: tt.bodySmall?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        color: cs.primary,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(4),
                                  child: LinearProgressIndicator(
                                    value: 0.85,
                                    backgroundColor: cs.outline.withOpacity(0.15),
                                    color: cs.primary,
                                    minHeight: 6,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Mission & Values
                        Text(
                          'Mission Statement',
                          style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        GlassmorphicDecorator.wrap(
                          context: context,
                          color: cs.surfaceContainerHighest,
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Text(
                              'Accelerate capability development and build agentic software solutions with premium human-AI operating heuristics.',
                              style: tt.bodyMedium?.copyWith(
                                fontStyle: FontStyle.italic,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Values Chips
                        Text(
                          'Core Professional Values',
                          style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: identity.coreValues.map((value) {
                            return Chip(
                              key: ValueKey('value_${value}_chip'),
                              avatar: Icon(Icons.star_rounded,
                                  size: 16, color: cs.primary),
                              label: Text(value),
                              backgroundColor: cs.primary.withOpacity(0.08),
                              side: BorderSide(
                                  color: cs.outline.withOpacity(0.15)),
                            );
                          }).toList(),
                        ),
                        const SizedBox(height: 24),
                      ],
                    );
                  },
                ),

                // Gap Analysis Loading/Error states
                gapState.when(
                  loading: () => const Center(
                    child: Padding(
                      padding: EdgeInsets.all(16.0),
                      child: CircularProgressIndicator(),
                    ),
                  ),
                  error: (err, stack) => ErrorStateWidget(
                    message: err.toString(),
                    onRetry: () => ref
                        .read(gapAnalysisControllerProvider.notifier)
                        .refreshData(),
                  ),
                  data: (gap) {
                    final double priorityPct = gap.priorityScore * 100;
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          'Capability Gap Analysis',
                          style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        GlassmorphicDecorator.wrap(
                          context: context,
                          color: cs.secondary,
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(Icons.warning_amber_rounded, color: cs.error, size: 14),
                                        const SizedBox(width: 4),
                                        Text(
                                          'URGENCY: ${gap.urgency.toUpperCase()}',
                                          style: tt.labelSmall?.copyWith(
                                            color: cs.secondary,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                    Text(
                                      'Priority: ${priorityPct.toInt()}%',
                                      style: tt.labelSmall?.copyWith(fontWeight: FontWeight.bold),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),
                                Text(
                                  gap.gapDescription,
                                  style: tt.bodyMedium,
                                ),
                                const Divider(height: 24),
                                Text(
                                  'RECOMMENDED STRATEGY',
                                  style: tt.labelSmall?.copyWith(
                                    color: cs.primary,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  gap.recommendsStrategy,
                                  style: tt.bodyMedium?.copyWith(fontWeight: FontWeight.w600),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Identity Evolution Timeline
                        Text(
                          'Identity Evolution Milestones',
                          style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        GlassmorphicDecorator.wrap(
                          context: context,
                          color: cs.surfaceContainerHighest,
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              children: [
                                _buildTimelineStep(
                                  context: context,
                                  title: 'Novice Learner',
                                  date: 'Nov 2025',
                                  desc: 'Initial onboarding completed with base technical values.',
                                  isCompleted: true,
                                ),
                                _buildTimelineDivider(context, true),
                                _buildTimelineStep(
                                  context: context,
                                  title: 'Explorer',
                                  date: 'Jan 2026',
                                  desc: 'Actively resolving Python variables and loops sprints.',
                                  isCompleted: true,
                                  isCurrent: true,
                                ),
                                _buildTimelineDivider(context, false),
                                _buildTimelineStep(
                                  context: context,
                                  title: 'Data Architect',
                                  date: 'Future Target',
                                  desc: 'Cognitive loop optimization targeting system architectures.',
                                  isCompleted: false,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTimelineStep({
    required BuildContext context,
    required String title,
    required String date,
    required String desc,
    required bool isCompleted,
    bool isCurrent = false,
  }) {
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            CircleAvatar(
              radius: 12,
              backgroundColor: isCompleted
                  ? (isCurrent ? cs.primary : cs.tertiary)
                  : cs.outline.withOpacity(0.3),
              child: Icon(
                isCompleted ? Icons.check_rounded : Icons.radio_button_unchecked_rounded,
                size: 14,
                color: Colors.white,
              ),
            ),
          ],
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    title,
                    style: tt.bodyMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: isCurrent ? cs.primary : null,
                    ),
                  ),
                  Text(
                    date,
                    style: tt.labelSmall?.copyWith(color: cs.onSurfaceVariant),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Text(
                desc,
                style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildTimelineDivider(BuildContext context, bool isCompleted) {
    final cs = Theme.of(context).colorScheme;
    return Container(
      margin: const EdgeInsets.only(left: 11, top: 4, bottom: 4),
      alignment: Alignment.centerLeft,
      height: 24,
      width: 2,
      color: isCompleted ? cs.tertiary : cs.outline.withOpacity(0.3),
    );
  }
}
