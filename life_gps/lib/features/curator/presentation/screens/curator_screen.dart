import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/glassmorphism.dart';
import '../../../../core/widgets/error_state_widget.dart';
import '../../../../core/widgets/loading_widget.dart';
import '../controllers/curator_controller.dart';

class CuratorScreen extends ConsumerWidget {
  const CuratorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(curatorControllerProvider);
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Curator'),
        actions: [
          IconButton(
            key: const ValueKey('curator_refresh_button'),
            icon: const Icon(Icons.refresh_rounded),
            onPressed: () => ref.read(curatorControllerProvider.notifier).refreshBundle(),
          ),
        ],
      ),
      body: SafeArea(
        child: state.when(
          loading: () => const Padding(
            padding: EdgeInsets.all(16.0),
            child: LoadingWidget(itemCount: 4, itemHeight: 120),
          ),
          error: (err, stack) => ErrorStateWidget(
            message: err.toString(),
            onRetry: () => ref.read(curatorControllerProvider.notifier).refreshBundle(),
          ),
          data: (curator) {
            final bundle = curator.bundle;
            final candidates = curator.candidatesRanked;
            final explanation = curator.explanation;

            // Generate content categorizations
            final videos = candidates.where((c) => c['resource_type']?.toString().toLowerCase() == 'video' || c['resource_name']?.toString().toLowerCase().contains('video') == true).toList();
            final articles = candidates.where((c) => c['resource_type']?.toString().toLowerCase() == 'article' || c['resource_name']?.toString().toLowerCase().contains('doc') == true).toList();
            final projects = candidates.where((c) => c['resource_type']?.toString().toLowerCase() == 'project' || c['resource_name']?.toString().toLowerCase().contains('project') == true).toList();

            return RefreshIndicator(
              onRefresh: () => ref.read(curatorControllerProvider.notifier).refreshBundle(),
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Active Recommended Bundle Cover Block
                    Container(
                      height: 180,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [cs.primary.withOpacity(0.8), cs.secondary.withOpacity(0.8)],
                        ),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: Colors.white24,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              'ACTIVE INTERVENTION PATHWAY',
                              style: tt.labelSmall?.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            bundle['name']?.toString() ?? 'Core Skill Intervention Bundle',
                            style: tt.headlineMedium?.copyWith(fontWeight: FontWeight.bold, color: Colors.white),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Estimated duration: ${bundle['estimated_completion_time_minutes'] ?? 45} mins',
                            style: tt.bodySmall?.copyWith(color: Colors.white70),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Explainability Card
                    if (explanation != null) ...[
                      Text(
                        'Why this curation?',
                        style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),
                      GlassmorphicDecorator.wrap(
                        context: context,
                        color: cs.tertiary,
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(Icons.psychology_rounded, color: cs.tertiary, size: 24),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      explanation.decision,
                                      style: tt.bodyMedium?.copyWith(fontWeight: FontWeight.w600),
                                    ),
                                  ),
                                ],
                              ),
                              const Divider(height: 20),
                              Text(
                                'ACTIVE SKILL GAPS RESOLVED',
                                style: tt.labelSmall?.copyWith(
                                  color: cs.tertiary,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                explanation.evidence,
                                style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                              ),
                              const SizedBox(height: 12),
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    'Alternative Evaluated:',
                                    style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant),
                                  ),
                                  Text(
                                    explanation.alternative,
                                    style: tt.bodySmall?.copyWith(fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 24),
                    ],

                    // Netflix-Style Horizontal Tracks
                    _buildTrackSection(
                      context: context,
                      title: 'Video Lectures',
                      items: videos.isNotEmpty ? videos : candidates,
                      icon: Icons.video_library_rounded,
                    ),
                    const SizedBox(height: 20),

                    _buildTrackSection(
                      context: context,
                      title: 'Documentation & Guides',
                      items: articles.isNotEmpty ? articles : candidates,
                      icon: Icons.article_rounded,
                    ),
                    const SizedBox(height: 20),

                    _buildTrackSection(
                      context: context,
                      title: 'Hands-on Code Projects',
                      items: projects.isNotEmpty ? projects : candidates,
                      icon: Icons.terminal_rounded,
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

  Widget _buildTrackSection({
    required BuildContext context,
    required String title,
    required List<Map<String, dynamic>> items,
    required IconData icon,
  }) {
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          children: [
            Icon(icon, size: 20, color: cs.primary),
            const SizedBox(width: 8),
            Text(
              title,
              style: tt.titleMedium?.copyWith(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 12),
        SizedBox(
          height: 160,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            separatorBuilder: (_, __) => const SizedBox(width: 12),
            itemBuilder: (context, index) {
              final item = items[index];
              final score = (item['score'] as num?)?.toDouble() ?? 0.90;

              return SizedBox(
                width: 240,
                child: GlassmorphicDecorator.wrap(
                  context: context,
                  color: cs.surface,
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: cs.primary.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: Text(
                                item['resource_type']?.toString() ?? 'Video',
                                style: tt.labelSmall?.copyWith(color: cs.primary, fontWeight: FontWeight.bold),
                              ),
                            ),
                            Text(
                              '⭐ ${(score * 5.0).toStringAsFixed(1)}',
                              style: tt.labelSmall?.copyWith(fontWeight: FontWeight.bold, color: Colors.amber),
                            ),
                          ],
                        ),
                        const Spacer(),
                        Text(
                          item['resource_name']?.toString() ?? item['title']?.toString() ?? 'Learning Resource',
                          style: tt.bodyMedium?.copyWith(fontWeight: FontWeight.bold),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 6),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              'Time: 35 mins',
                              style: tt.labelSmall?.copyWith(color: cs.onSurfaceVariant),
                            ),
                            Text(
                              '+8% Python',
                              style: tt.labelSmall?.copyWith(fontWeight: FontWeight.bold, color: cs.tertiary),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
