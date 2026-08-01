import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../di/providers.dart';
import '../workflow/workflow_state.dart';

class ErrorBanner extends ConsumerWidget {
  const ErrorBanner({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final workflowState = ref.watch(workflowControllerProvider);
    final cs = Theme.of(context).colorScheme;

    String? message;
    Color? bgColor;
    IconData? icon;

    if (workflowState is Failed) {
      message = 'AI Connection Interrupted. Retrying...';
      bgColor = cs.errorContainer.withOpacity(0.9);
      icon = Icons.sync_problem_rounded;
    }

    if (message == null) {
      return const SizedBox.shrink();
    }

    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      color: bgColor,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 20, color: cs.onErrorContainer),
          const SizedBox(width: 8),
          Text(
            message,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: cs.onErrorContainer,
                  fontWeight: FontWeight.w600,
                ),
          ),
        ],
      ),
    );
  }
}
