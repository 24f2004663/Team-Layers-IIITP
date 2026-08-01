import 'package:flutter/material.dart';

enum AppButtonVariant { primary, secondary, ghost, danger }

enum AppButtonSize { small, medium, large }

/// Life-GPS styled button supporting primary, secondary, ghost, and danger variants.
class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final AppButtonVariant variant;
  final AppButtonSize size;
  final IconData? leadingIcon;
  final IconData? trailingIcon;
  final bool isLoading;
  final bool fullWidth;

  const AppButton({
    super.key,
    required this.label,
    this.onPressed,
    this.variant = AppButtonVariant.primary,
    this.size = AppButtonSize.medium,
    this.leadingIcon,
    this.trailingIcon,
    this.isLoading = false,
    this.fullWidth = false,
  });

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final child = _buildChild(cs);

    Widget button;
    switch (variant) {
      case AppButtonVariant.primary:
        button = FilledButton(
          onPressed: isLoading ? null : onPressed,
          style: _style(size),
          child: child,
        );
      case AppButtonVariant.secondary:
        button = OutlinedButton(
          onPressed: isLoading ? null : onPressed,
          style: _style(size),
          child: child,
        );
      case AppButtonVariant.ghost:
        button = TextButton(
          onPressed: isLoading ? null : onPressed,
          style: _style(size),
          child: child,
        );
      case AppButtonVariant.danger:
        button = FilledButton(
          onPressed: isLoading ? null : onPressed,
          style: FilledButton.styleFrom(
            backgroundColor: cs.error,
            foregroundColor: cs.onError,
          ).merge(_style(size)),
          child: child,
        );
    }

    return fullWidth ? SizedBox(width: double.infinity, child: button) : button;
  }

  Widget _buildChild(ColorScheme cs) {
    if (isLoading) {
      return SizedBox(
        width: 18,
        height: 18,
        child: CircularProgressIndicator(strokeWidth: 2, color: cs.onPrimary),
      );
    }

    final children = <Widget>[];
    if (leadingIcon != null) {
      children.addAll(
          [Icon(leadingIcon, size: _iconSize), const SizedBox(width: 8)]);
    }
    children.add(Text(label));
    if (trailingIcon != null) {
      children.addAll(
          [const SizedBox(width: 8), Icon(trailingIcon, size: _iconSize)]);
    }

    return Row(mainAxisSize: MainAxisSize.min, children: children);
  }

  ButtonStyle _style(AppButtonSize s) {
    final padding = switch (s) {
      AppButtonSize.small =>
        const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      AppButtonSize.medium =>
        const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
      AppButtonSize.large =>
        const EdgeInsets.symmetric(horizontal: 32, vertical: 18),
    };
    return ButtonStyle(padding: WidgetStateProperty.all(padding));
  }

  double get _iconSize => switch (size) {
        AppButtonSize.small => 16,
        AppButtonSize.medium => 18,
        AppButtonSize.large => 20,
      };
}
