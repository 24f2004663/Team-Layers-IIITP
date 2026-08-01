import 'package:flutter/material.dart';

/// Life-GPS brand color palette.
class AppColors {
  AppColors._();

  // ─── Brand ───────────────────────────────────────────────────────────────
  static const Color primaryViolet = Color(0xFF6C63FF);
  static const Color primaryVioletLight = Color(0xFF9D97FF);
  static const Color primaryVioletDark = Color(0xFF4A42CC);

  static const Color accentCyan = Color(0xFF00D4FF);
  static const Color accentCyanLight = Color(0xFF66E3FF);
  static const Color accentCyanDark = Color(0xFF009ABB);

  // ─── Surfaces (Dark Mode) ────────────────────────────────────────────────
  static const Color surfaceDark = Color(0xFF0F0F1A);
  static const Color surfaceDark2 = Color(0xFF161624);
  static const Color surfaceDark3 = Color(0xFF1E1E30);
  static const Color surfaceDark4 = Color(0xFF252540);
  static const Color cardDark = Color(0xFF1C1C2E);

  // ─── Surfaces (Light Mode) ───────────────────────────────────────────────
  static const Color surfaceLight = Color(0xFFF5F5FF);
  static const Color surfaceLight2 = Color(0xFFEEEEFF);
  static const Color cardLight = Color(0xFFFFFFFF);

  // ─── Semantic ─────────────────────────────────────────────────────────────
  static const Color success = Color(0xFF00D68F);
  static const Color successLight = Color(0xFF66FFCC);
  static const Color warning = Color(0xFFFFB547);
  static const Color warningLight = Color(0xFFFFD999);
  static const Color error = Color(0xFFFF4D6A);
  static const Color errorLight = Color(0xFFFF9AAA);
  static const Color info = Color(0xFF00B8FF);

  // ─── Text ─────────────────────────────────────────────────────────────────
  static const Color textPrimaryDark = Color(0xFFF0F0FF);
  static const Color textSecondaryDark = Color(0xFFAAAAAA);
  static const Color textMutedDark = Color(0xFF666680);

  static const Color textPrimaryLight = Color(0xFF0A0A1A);
  static const Color textSecondaryLight = Color(0xFF444466);
  static const Color textMutedLight = Color(0xFF888899);

  // ─── Gradients ────────────────────────────────────────────────────────────
  static const Gradient primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [primaryViolet, accentCyan],
  );

  static const Gradient darkCardGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [surfaceDark3, surfaceDark4],
  );

  static const Gradient successGradient = LinearGradient(
    colors: [Color(0xFF00D68F), Color(0xFF00B8FF)],
  );
}
