import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

/// Displays a labelled circular or linear progress indicator card.
class ProgressCard extends StatelessWidget {
  final String title;
  final String? subtitle;
  final double progress; // 0.0–1.0
  final Color? progressColor;
  final bool showPercentage;

  const ProgressCard({
    super.key,
    required this.title,
    required this.progress,
    this.subtitle,
    this.progressColor,
    this.showPercentage = true,
  });

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final tt = Theme.of(context).textTheme;
    final color = progressColor ?? AppColors.primaryViolet;
    final pct = (progress * 100).toStringAsFixed(0);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title,
                    style:
                        tt.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                if (showPercentage)
                  Text('$pct%',
                      style: tt.labelMedium?.copyWith(
                          color: color, fontWeight: FontWeight.w700)),
              ],
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 4),
              Text(subtitle!,
                  style: tt.bodySmall?.copyWith(color: cs.onSurfaceVariant)),
            ],
            const SizedBox(height: 12),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: progress.clamp(0.0, 1.0),
                minHeight: 8,
                backgroundColor: color.withOpacity(0.15),
                valueColor: AlwaysStoppedAnimation<Color>(color),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
