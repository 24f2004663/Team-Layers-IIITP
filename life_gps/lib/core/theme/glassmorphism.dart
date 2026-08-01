import 'dart:ui';
import 'package:flutter/material.dart';

class GlassmorphicDecorator {
  GlassmorphicDecorator._();

  static BoxDecoration decoration({
    required BuildContext context,
    required Color color,
    double borderRadius = 16.0,
    double borderOpacity = 0.15,
  }) {
    final cs = Theme.of(context).colorScheme;
    return BoxDecoration(
      borderRadius: BorderRadius.circular(borderRadius),
      gradient: LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          color.withOpacity(0.08),
          color.withOpacity(0.02),
        ],
      ),
      border: Border.all(
        color: cs.outline.withOpacity(borderOpacity),
        width: 1.0,
      ),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.05),
          blurRadius: 10,
          offset: const Offset(0, 4),
        ),
      ],
    );
  }

  static Widget wrap({
    required BuildContext context,
    required Widget child,
    required Color color,
    double borderRadius = 16.0,
    double blurX = 12.0,
    double blurY = 12.0,
    double borderOpacity = 0.15,
  }) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blurX, sigmaY: blurY),
        child: Container(
          decoration: decoration(
            context: context,
            color: color,
            borderRadius: borderRadius,
            borderOpacity: borderOpacity,
          ),
          child: child,
        ),
      ),
    );
  }
}
