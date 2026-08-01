import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/widgets/error_state_widget.dart';
import '../../../../core/widgets/loading_widget.dart';
import '../controllers/planner_controller.dart';

class PlannerScreen extends ConsumerStatefulWidget {
  const PlannerScreen({super.key});

  @override
  ConsumerState<PlannerScreen> createState() => _PlannerScreenState();
}

class _PlannerScreenState extends ConsumerState<PlannerScreen> {
  bool _isWeekly = false;
  List<Map<String, dynamic>> _localDailyTasks = [];
  bool _isInitialized = false;

  void _initializeTasks(Map<String, dynamic> executionPlan) {
    if (!_isInitialized) {
      final List<dynamic> rawTasks = executionPlan['tasks'] as List? ?? [];
      _localDailyTasks = rawTasks.map((t) => Map<String, dynamic>.from(t as Map)).toList();
      _isInitialized = true;
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(plannerControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Planner Center'),
        actions: [
          IconButton(
            key: const ValueKey('planner_refresh_button'),
            icon: const Icon(Icons.refresh_rounded),
            onPressed: () {
              setState(() {
                _isInitialized = false;
              });
              ref.read(plannerControllerProvider.notifier).refreshPlan(weekly: _isWeekly);
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Daily / Weekly Selector Switch
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
              child: SegmentedButton<bool>(
                key: const ValueKey('planner_view_selector'),
                segments: const [
                  ButtonSegment<bool>(
                    value: false,
                    label: Text('Daily Timeline'),
                    icon: Icon(Icons.view_day_rounded),
                  ),
                  ButtonSegment<bool>(
                    value: true,
                    label: Text('Weekly Objectives'),
                    icon: Icon(Icons.view_week_rounded),
                  ),
                ],
                selected: {_isWeekly},
                onSelectionChanged: (Set<bool> val) {
                  setState(() {
                    _isWeekly = val.first;
                    _isInitialized = false;
                  });
                  ref.read(plannerControllerProvider.notifier).refreshPlan(weekly: _isWeekly);
                },
              ),
            ),

            // Main Content Area
            Expanded(
              child: state.when(
                loading: () => const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: LoadingWidget(itemCount: 4, itemHeight: 110),
                ),
                error: (err, stack) => ErrorStateWidget(
                  message: err.toString(),
                  onRetry: () {
                    setState(() {
                      _isInitialized = false;
                    });
                    ref.read(plannerControllerProvider.notifier).refreshPlan(weekly: _isWeekly);
                  },
                ),
                data: (plan) {
                  if (_isWeekly) {
                    final weeklyGoals = plan.weeklyObjectives;
                    return RefreshIndicator(
                      onRefresh: () => ref.read(plannerControllerProvider.notifier).refreshPlan(weekly: true),
                      child: weeklyGoals.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.calendar_month_rounded, size: 64, color: cs.outline),
                                  const SizedBox(height: 12),
                                  Text(
                                    'No objectives set for this week',
                                    style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            )
                          : ListView.separated(
                              padding: const EdgeInsets.all(16.0),
                              itemCount: weeklyGoals.length,
                              separatorBuilder: (context, index) => const SizedBox(height: 12),
                              itemBuilder: (context, index) {
                                final obj = weeklyGoals[index];
                                return GlassmorphicDecorator.wrap(
                                  context: context,
                                  color: cs.secondary,
                                  child: ListTile(
                                    leading: CircleAvatar(
                                      backgroundColor: cs.secondary.withOpacity(0.1),
                                      child: Icon(Icons.star_rounded, color: cs.secondary),
                                    ),
                                    title: Text(
                                      obj,
                                      style: tt.bodyLarge?.copyWith(fontWeight: FontWeight.bold),
                                    ),
                                    subtitle: const Text('Priority Track Milestone'),
                                  ),
                                );
                              },
                            ),
                    );
                  }

                  // Daily Timeline / Tasks
                  final execution = plan.executionPlan;
                  _initializeTasks(execution);

                  final List<dynamic> rawSlots = execution['focus_time_slots'] as List? ?? [];
                  final slots = List<String>.from(rawSlots);
                  final health = execution['health_score'] as Map? ?? {};
                  final workloadBal = (health['workload_balance'] as num?)?.toDouble() ?? 0.85;
                  final estimatedSuccess = (health['estimated_success_probability'] as num?)?.toDouble() ?? 0.90;

                  return RefreshIndicator(
                    onRefresh: () async {
                      setState(() {
                        _isInitialized = false;
                      });
                      await ref.read(plannerControllerProvider.notifier).refreshPlan(weekly: false);
                    },
                    child: SingleChildScrollView(
                      physics: const AlwaysScrollableScrollPhysics(),
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // Daily Stats Summary Cards
                          Row(
                            children: [
                              Expanded(
                                child: GlassmorphicDecorator.wrap(
                                  context: context,
                                  color: cs.primary,
                                  child: Padding(
                                    padding: const EdgeInsets.all(12.0),
                                    child: Column(
                                      children: [
                                        Text('Schedule Health', style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
                                        const SizedBox(height: 4),
                                        Text('${(workloadBal * 100).toInt()}%', style: tt.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: cs.primary)),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: GlassmorphicDecorator.wrap(
                                  context: context,
                                  color: cs.tertiary,
                                  child: Padding(
                                    padding: const EdgeInsets.all(12.0),
                                    child: Column(
                                      children: [
                                        Text('Success Forecast', style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
                                        const SizedBox(height: 4),
                                        Text('${(estimatedSuccess * 100).toInt()}%', style: tt.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: cs.tertiary)),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 24),

                          // Focus Blocks Title
                          Text(
                            'Focus Time Slots Mapped',
                            style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 12),
                          if (slots.isEmpty)
                            Text(
                              'No focus blocks scheduled for today.',
                              style: tt.bodyMedium?.copyWith(color: cs.onSurfaceVariant),
                            )
                          else
                            Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: slots.map((slot) {
                                return Chip(
                                  avatar: Icon(Icons.access_time_rounded, size: 16, color: cs.primary),
                                  label: Text(slot),
                                  backgroundColor: cs.primary.withOpacity(0.08),
                                  side: BorderSide(color: cs.outline.withOpacity(0.15)),
                                );
                              }).toList(),
                            ),
                          const SizedBox(height: 24),

                          // Interactive Drag-and-Drop Tasks Title
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Interactive Agenda (Drag-to-Reschedule)',
                                style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                              ),
                              Text(
                                'Press & Hold',
                                style: tt.labelSmall?.copyWith(color: cs.onSurfaceVariant),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          if (_localDailyTasks.isEmpty)
                            Text(
                              'No tasks resolved for today.',
                              style: tt.bodyMedium?.copyWith(color: cs.onSurfaceVariant),
                            )
                          else
                            ListView.separated(
                              shrinkWrap: true,
                              physics: const NeverScrollableScrollPhysics(),
                              itemCount: _localDailyTasks.length,
                              separatorBuilder: (context, index) => const SizedBox(height: 12),
                              itemBuilder: (context, index) {
                                final task = _localDailyTasks[index];
                                final isDone = task['is_completed'] as bool? ?? false;

                                // Build Drag and Drop targets
                                return DragTarget<int>(
                                  onWillAcceptWithDetails: (details) => details.data != index,
                                  onAcceptWithDetails: (details) {
                                    setState(() {
                                      final draggedItem = _localDailyTasks.removeAt(details.data);
                                      _localDailyTasks.insert(index, draggedItem);
                                    });
                                  },
                                  builder: (context, candidateData, rejectedData) {
                                    final isHovered = candidateData.isNotEmpty;

                                    return LongPressDraggable<int>(
                                      data: index,
                                      feedback: SizedBox(
                                        width: MediaQuery.of(context).size.width - 32,
                                        child: Material(
                                          color: Colors.transparent,
                                          child: GlassmorphicDecorator.wrap(
                                            context: context,
                                            color: cs.primary.withOpacity(0.8),
                                            child: ListTile(
                                              title: Text(task['title']?.toString() ?? 'Daily Agenda Task', style: const TextStyle(fontWeight: FontWeight.bold)),
                                              leading: const Icon(Icons.drag_indicator_rounded),
                                            ),
                                          ),
                                        ),
                                      ),
                                      childWhenDragging: Opacity(
                                        opacity: 0.3,
                                        child: GlassmorphicDecorator.wrap(
                                          context: context,
                                          color: cs.surface,
                                          child: ListTile(
                                            title: Text(task['title']?.toString() ?? 'Daily Agenda Task'),
                                          ),
                                        ),
                                      ),
                                      child: AnimatedContainer(
                                        duration: const Duration(milliseconds: 200),
                                        decoration: BoxDecoration(
                                          borderRadius: BorderRadius.circular(16),
                                          border: isHovered ? Border.all(color: cs.primary, width: 2) : null,
                                        ),
                                        child: GlassmorphicDecorator.wrap(
                                          context: context,
                                          color: cs.surface,
                                          child: CheckboxListTile(
                                            key: ValueKey('task_${task['task_id'] ?? index}_tile'),
                                            value: isDone,
                                            onChanged: (val) {
                                              setState(() {
                                                _localDailyTasks[index]['is_completed'] = val ?? false;
                                              });
                                            },
                                            title: Text(
                                              task['title']?.toString() ?? 'Daily Agenda Task',
                                              style: tt.bodyLarge?.copyWith(
                                                fontWeight: FontWeight.bold,
                                                decoration: isDone ? TextDecoration.lineThrough : null,
                                              ),
                                            ),
                                            subtitle: Text(
                                              'Priority: ${(task['weight'] ?? 1.0).toString()}',
                                              style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                                            ),
                                            secondary: CircleAvatar(
                                              backgroundColor: (isDone ? cs.tertiary : cs.primary).withOpacity(0.1),
                                              child: Icon(
                                                isDone ? Icons.task_alt_rounded : Icons.drag_indicator_rounded,
                                                color: isDone ? cs.tertiary : cs.primary,
                                              ),
                                            ),
                                          ),
                                        ),
                                      ),
                                    );
                                  },
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
    );
  }
}
