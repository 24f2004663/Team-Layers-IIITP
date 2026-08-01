import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/widgets/error_state_widget.dart';
import '../controllers/behavior_controller.dart';

class BehaviorScreen extends ConsumerWidget {
  const BehaviorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(behaviorControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Behavioral Routines'),
        actions: [
          IconButton(
            key: const ValueKey('behavior_refresh_button'),
            icon: const Icon(Icons.refresh_rounded),
            onPressed: () =>
                ref.read(behaviorControllerProvider.notifier).refreshData(),
          ),
        ],
      ),
      body: SafeArea(
        child: state.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, stack) => ErrorStateWidget(
            message: err.toString(),
            onRetry: () =>
                ref.read(behaviorControllerProvider.notifier).refreshData(),
          ),
          data: (behavior) {
            final habits = behavior.habits;
            final cognitive = behavior.cognitivePatterns;
            final energy = behavior.energyLevels;

            return RefreshIndicator(
              onRefresh: () =>
                  ref.read(behaviorControllerProvider.notifier).refreshData(),
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Energy prediction levels
                    Text(
                      'Energy & Focus Forecasts',
                      style:
                          tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    GlassmorphicDecorator.wrap(
                      context: context,
                      color: cs.primary,
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: energy.entries.map((entry) {
                            return Padding(
                              padding:
                                  const EdgeInsets.symmetric(vertical: 8.0),
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
                                      borderRadius: BorderRadius.circular(4),
                                      child: LinearProgressIndicator(
                                        value: entry.value,
                                        backgroundColor:
                                            cs.outline.withOpacity(0.15),
                                        color: entry.value > 0.7
                                            ? cs.primary
                                            : cs.secondary,
                                        minHeight: 8,
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: 12),
                                  Text(
                                    '${(entry.value * 100).toInt()}%',
                                    style: tt.bodySmall
                                        ?.copyWith(fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Habit Streaks Grid
                    Text(
                      'Habit Consistency Matrix',
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
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: ['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((day) {
                                return SizedBox(
                                  width: 32,
                                  child: Text(
                                    day,
                                    style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold),
                                    textAlign: TextAlign.center,
                                  ),
                                );
                              }).toList(),
                            ),
                            const SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: List.generate(7, (idx) {
                                final isDone = idx < 5; // Simulating Monday-Friday completed
                                return Container(
                                  width: 32,
                                  height: 32,
                                  decoration: BoxDecoration(
                                    color: isDone ? cs.tertiary : cs.outline.withOpacity(0.15),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Icon(
                                    isDone ? Icons.check_rounded : Icons.close_rounded,
                                    size: 14,
                                    color: isDone ? Colors.white : cs.onSurfaceVariant.withOpacity(0.5),
                                  ),
                                );
                              }),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Active Habit cards
                    Text(
                      'Target Routine Habits',
                      style:
                          tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    if (habits.isEmpty)
                      Text(
                        'No routine habits initialized yet.',
                        style:
                            tt.bodyMedium?.copyWith(color: cs.onSurfaceVariant),
                      )
                    else
                      ListView.separated(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: habits.length,
                        separatorBuilder: (context, index) =>
                            const SizedBox(height: 12),
                        itemBuilder: (context, index) {
                          final key = habits.keys.elementAt(index);
                          final dynamic habitVal = habits[key];
                          final habitMap = habitVal is Map
                              ? Map<String, dynamic>.from(habitVal)
                              : {};
                          final streak = habitMap['streak'] as int? ?? 0;
                          final completed =
                              habitMap['completed_today'] as bool? ?? false;

                          return GlassmorphicDecorator.wrap(
                            context: context,
                            color: completed ? cs.tertiary : cs.surface,
                            child: ListTile(
                              key: ValueKey('habit_${key}_tile'),
                              leading: CircleAvatar(
                                backgroundColor:
                                    (completed ? cs.tertiary : cs.primary)
                                        .withOpacity(0.1),
                                child: Icon(
                                  completed
                                      ? Icons.check_circle_rounded
                                      : Icons.radio_button_unchecked_rounded,
                                  color: completed ? cs.tertiary : cs.primary,
                                ),
                              ),
                              title: Text(
                                key.toUpperCase(),
                                style: tt.bodyLarge
                                    ?.copyWith(fontWeight: FontWeight.bold),
                              ),
                              subtitle: Text(
                                completed
                                    ? 'Completed for today!'
                                    : 'Pending action target',
                                style: tt.bodySmall
                                    ?.copyWith(color: cs.onSurfaceVariant),
                              ),
                              trailing: Container(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 4),
                                decoration: BoxDecoration(
                                  color: cs.primary.withOpacity(0.15),
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: Text(
                                  '🔥 $streak days',
                                  style: tt.labelSmall?.copyWith(
                                    color: cs.primary,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    const SizedBox(height: 24),

                    // Cognitive Patterns
                    Text(
                      'Cognitive Bias & Patterns',
                      style:
                          tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: cognitive.map((pattern) {
                        return Chip(
                          avatar: Icon(Icons.psychology_rounded,
                              size: 16, color: cs.secondary),
                          label: Text(pattern),
                          backgroundColor: cs.secondary.withOpacity(0.08),
                          side: BorderSide(color: cs.outline.withOpacity(0.15)),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
