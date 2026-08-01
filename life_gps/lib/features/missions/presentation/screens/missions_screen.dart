import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/widgets/error_state_widget.dart';
import '../../../../core/widgets/loading_widget.dart';
import '../controllers/mission_controller.dart';

class MissionsScreen extends ConsumerStatefulWidget {
  const MissionsScreen({super.key});

  @override
  ConsumerState<MissionsScreen> createState() => _MissionsScreenState();
}

class _MissionsScreenState extends ConsumerState<MissionsScreen> {
  String _searchQuery = '';
  bool _sortByPriority = true;
  String _filterPriority = 'ALL'; // 'ALL', 'HIGH', 'MEDIUM'

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(missionControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mission Center'),
      ),
      body: SafeArea(
        child: state.when(
          loading: () => const Padding(
            padding: EdgeInsets.all(16.0),
            child: LoadingWidget(itemCount: 4, itemHeight: 90),
          ),
          error: (err, stack) => ErrorStateWidget(
            message: err.toString(),
            onRetry: () => ref.read(missionControllerProvider.notifier).refreshMissions(),
          ),
          data: (missions) {
            // Apply filtering
            final filtered = missions.where((m) {
              final matchSearch = m.title.toLowerCase().contains(_searchQuery.toLowerCase()) ||
                  m.description.toLowerCase().contains(_searchQuery.toLowerCase());
              
              if (!matchSearch) return false;

              if (_filterPriority == 'HIGH') return m.priority > 0.7;
              if (_filterPriority == 'MEDIUM') return m.priority <= 0.7;
              return true;
            }).toList();

            // Sort
            if (_sortByPriority) {
              filtered.sort((a, b) => b.priority.compareTo(a.priority));
            } else {
              filtered.sort((a, b) => a.title.compareTo(b.title));
            }

            return RefreshIndicator(
              onRefresh: () => ref.read(missionControllerProvider.notifier).refreshMissions(),
              child: Column(
                children: [
                  // Search & Filter controls
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                key: const ValueKey('search_missions_field'),
                                decoration: InputDecoration(
                                  hintText: 'Search missions...',
                                  prefixIcon: const Icon(Icons.search_rounded),
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                                ),
                                onChanged: (val) {
                                  setState(() {
                                    _searchQuery = val;
                                  });
                                },
                              ),
                            ),
                            const SizedBox(width: 12),
                            IconButton.filledTonal(
                              key: const ValueKey('sort_missions_button'),
                              icon: Icon(
                                _sortByPriority ? Icons.sort_rounded : Icons.sort_by_alpha_rounded,
                              ),
                              onPressed: () {
                                setState(() {
                                  _sortByPriority = !_sortByPriority;
                                });
                              },
                              tooltip: 'Toggle Sort Order',
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        // Priority Filter Segmented Row
                        Row(
                          children: [
                            Text(
                              'Filter Priority: ',
                              style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold),
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Wrap(
                                spacing: 8,
                                children: ['ALL', 'HIGH', 'MEDIUM'].map((type) {
                                  final isSelected = _filterPriority == type;
                                  return ChoiceChip(
                                    label: Text(type),
                                    selected: isSelected,
                                    onSelected: (val) {
                                      if (val) {
                                        setState(() {
                                          _filterPriority = type;
                                        });
                                      }
                                    },
                                    selectedColor: cs.primaryContainer,
                                    labelStyle: tt.labelSmall?.copyWith(
                                      fontWeight: FontWeight.bold,
                                      color: isSelected ? cs.onPrimaryContainer : cs.onSurface,
                                    ),
                                  );
                                }).toList(),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  // Missions List
                  Expanded(
                    child: filtered.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.rocket_rounded, size: 64, color: cs.outline),
                                const SizedBox(height: 12),
                                Text(
                                  'No active missions found',
                                  style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                                ),
                              ],
                            ),
                          )
                        : ListView.separated(
                            padding: const EdgeInsets.only(left: 16, right: 16, bottom: 24),
                            itemCount: filtered.length,
                            separatorBuilder: (context, index) => const SizedBox(height: 12),
                            itemBuilder: (context, index) {
                              final mission = filtered[index];
                              final isHighPriority = mission.priority > 0.7;

                              return GlassmorphicDecorator.wrap(
                                context: context,
                                color: isHighPriority ? cs.primary : cs.surface,
                                child: Theme(
                                  data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
                                  child: ExpansionTile(
                                    key: ValueKey('mission_${mission.id}_tile'),
                                    leading: CircleAvatar(
                                      backgroundColor: (isHighPriority ? cs.primary : cs.secondary).withOpacity(0.1),
                                      child: Icon(Icons.rocket_launch_rounded, color: isHighPriority ? cs.primary : cs.secondary, size: 20),
                                    ),
                                    title: Text(
                                      mission.title,
                                      style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                                    ),
                                    subtitle: Padding(
                                      padding: const EdgeInsets.only(top: 4.0),
                                      child: Wrap(
                                        spacing: 6,
                                        runSpacing: 4,
                                        children: mission.targetSkills.map((s) {
                                          return Container(
                                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                            decoration: BoxDecoration(
                                              color: cs.primary.withOpacity(0.1),
                                              borderRadius: BorderRadius.circular(10),
                                            ),
                                            child: Text(
                                              s,
                                              style: tt.labelSmall?.copyWith(color: cs.primary),
                                            ),
                                          );
                                        }).toList(),
                                      ),
                                    ),
                                    trailing: Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: (isHighPriority ? cs.error : cs.secondary).withOpacity(0.15),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Text(
                                        isHighPriority ? 'HIGH' : 'MEDIUM',
                                        style: tt.labelSmall?.copyWith(
                                          color: isHighPriority ? cs.error : cs.secondary,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),
                                    children: [
                                      Padding(
                                        padding: const EdgeInsets.only(left: 16.0, right: 16.0, bottom: 16.0),
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.stretch,
                                          children: [
                                            const Divider(height: 16),
                                            Text(
                                              'MISSION DESCRIPTION',
                                              style: tt.labelSmall?.copyWith(
                                                color: cs.primary,
                                                fontWeight: FontWeight.bold,
                                              ),
                                            ),
                                            const SizedBox(height: 4),
                                            Text(
                                              mission.description,
                                              style: tt.bodyMedium,
                                            ),
                                            const SizedBox(height: 16),
                                            
                                            // Mission Dependency Visualizer
                                            Text(
                                              'CAPABILITY DEPENDENCY PATH',
                                              style: tt.labelSmall?.copyWith(
                                                color: cs.secondary,
                                                fontWeight: FontWeight.bold,
                                              ),
                                            ),
                                            const SizedBox(height: 8),
                                            Row(
                                              children: [
                                                Icon(Icons.check_circle_rounded, color: cs.tertiary, size: 16),
                                                const SizedBox(width: 6),
                                                Text(
                                                  'Prerequisite: Basics and Syntax Fundamentals',
                                                  style: tt.bodySmall?.copyWith(decoration: TextDecoration.lineThrough),
                                                ),
                                              ],
                                            ),
                                            const SizedBox(height: 4),
                                            Row(
                                              children: [
                                                Icon(Icons.play_circle_outline_rounded, color: cs.primary, size: 16),
                                                const SizedBox(width: 6),
                                                Text(
                                                  'Current: ${mission.title}',
                                                  style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold, color: cs.primary),
                                                ),
                                              ],
                                            ),
                                            const SizedBox(height: 4),
                                            Row(
                                              children: [
                                                Icon(Icons.radio_button_unchecked_rounded, color: cs.outline, size: 16),
                                                const SizedBox(width: 6),
                                                Text(
                                                  'Next Target: Performance Benchmarking Sprint',
                                                  style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                                                ),
                                              ],
                                            ),
                                            const SizedBox(height: 16),

                                            // Success Probability progress bar
                                            Row(
                                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                              children: [
                                                Text('Success Probability Rating', style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
                                                Text('92.5%', style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold, color: cs.tertiary)),
                                              ],
                                            ),
                                            const SizedBox(height: 6),
                                            ClipRRect(
                                              borderRadius: BorderRadius.circular(4),
                                              child: LinearProgressIndicator(
                                                value: 0.925,
                                                minHeight: 6,
                                                backgroundColor: cs.outline.withOpacity(0.15),
                                                color: cs.tertiary,
                                              ),
                                            ),
                                          ],
                                        ),
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
            );
          },
        ),
      ),
    );
  }
}
