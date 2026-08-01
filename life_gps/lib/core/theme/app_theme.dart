import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

/// Material 3 theme system for Life-GPS.
class AppTheme {
  AppTheme._();

  static ThemeData get dark => _buildDark();
  static ThemeData get light => _buildLight();

  static ThemeData _buildDark() {
    const colorScheme = ColorScheme(
      brightness: Brightness.dark,
      primary: AppColors.primaryViolet,
      onPrimary: Colors.white,
      primaryContainer: AppColors.primaryVioletDark,
      onPrimaryContainer: AppColors.primaryVioletLight,
      secondary: AppColors.accentCyan,
      onSecondary: AppColors.surfaceDark,
      secondaryContainer: AppColors.accentCyanDark,
      onSecondaryContainer: AppColors.accentCyanLight,
      tertiary: AppColors.success,
      onTertiary: AppColors.surfaceDark,
      tertiaryContainer: Color(0xFF003D2A),
      onTertiaryContainer: AppColors.successLight,
      error: AppColors.error,
      onError: Colors.white,
      errorContainer: Color(0xFF4D0015),
      onErrorContainer: AppColors.errorLight,
      surface: AppColors.surfaceDark,
      onSurface: AppColors.textPrimaryDark,
      surfaceContainerHighest: AppColors.surfaceDark4,
      onSurfaceVariant: AppColors.textSecondaryDark,
      outline: AppColors.textMutedDark,
      shadow: Colors.black,
      inverseSurface: AppColors.surfaceLight,
      onInverseSurface: AppColors.textPrimaryLight,
      inversePrimary: AppColors.primaryVioletDark,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: AppColors.surfaceDark,
      textTheme: _buildTextTheme(AppColors.textPrimaryDark),
      appBarTheme: _appBarTheme(colorScheme, AppColors.surfaceDark2),
      cardTheme: _cardTheme(AppColors.cardDark),
      inputDecorationTheme: _inputTheme(colorScheme, Brightness.dark),
      elevatedButtonTheme: _elevatedButtonTheme(colorScheme),
      outlinedButtonTheme: _outlinedButtonTheme(colorScheme),
      textButtonTheme: _textButtonTheme(colorScheme),
      chipTheme: _chipTheme(colorScheme),
      dividerTheme:
          DividerThemeData(color: AppColors.textMutedDark.withOpacity(0.3)),
      iconTheme: const IconThemeData(color: AppColors.textSecondaryDark),
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: AppColors.primaryViolet,
        foregroundColor: Colors.white,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: AppColors.surfaceDark2,
        indicatorColor: AppColors.primaryViolet.withOpacity(0.2),
        labelTextStyle: WidgetStateProperty.all(
          GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w500),
        ),
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: AppColors.surfaceDark2,
        selectedItemColor: AppColors.primaryViolet,
        unselectedItemColor: AppColors.textMutedDark,
      ),
    );
  }

  static ThemeData _buildLight() {
    const colorScheme = ColorScheme(
      brightness: Brightness.light,
      primary: AppColors.primaryViolet,
      onPrimary: Colors.white,
      primaryContainer: AppColors.surfaceLight2,
      onPrimaryContainer: AppColors.primaryVioletDark,
      secondary: AppColors.accentCyanDark,
      onSecondary: Colors.white,
      secondaryContainer: Color(0xFFCCF5FF),
      onSecondaryContainer: AppColors.accentCyanDark,
      tertiary: AppColors.success,
      onTertiary: Colors.white,
      tertiaryContainer: Color(0xFFCCFFEE),
      onTertiaryContainer: Color(0xFF00422F),
      error: AppColors.error,
      onError: Colors.white,
      errorContainer: Color(0xFFFFDADE),
      onErrorContainer: Color(0xFF410010),
      surface: AppColors.surfaceLight,
      onSurface: AppColors.textPrimaryLight,
      surfaceContainerHighest: AppColors.surfaceLight2,
      onSurfaceVariant: AppColors.textSecondaryLight,
      outline: AppColors.textMutedLight,
      shadow: Colors.black26,
      inverseSurface: AppColors.surfaceDark3,
      onInverseSurface: AppColors.textPrimaryDark,
      inversePrimary: AppColors.primaryVioletLight,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: AppColors.surfaceLight,
      textTheme: _buildTextTheme(AppColors.textPrimaryLight),
      appBarTheme: _appBarTheme(colorScheme, AppColors.surfaceLight),
      cardTheme: _cardTheme(AppColors.cardLight),
      inputDecorationTheme: _inputTheme(colorScheme, Brightness.light),
      elevatedButtonTheme: _elevatedButtonTheme(colorScheme),
      outlinedButtonTheme: _outlinedButtonTheme(colorScheme),
      textButtonTheme: _textButtonTheme(colorScheme),
      chipTheme: _chipTheme(colorScheme),
      dividerTheme:
          DividerThemeData(color: AppColors.textMutedLight.withOpacity(0.3)),
      iconTheme: const IconThemeData(color: AppColors.textSecondaryLight),
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: AppColors.primaryViolet,
        foregroundColor: Colors.white,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: AppColors.cardLight,
        indicatorColor: AppColors.primaryViolet.withOpacity(0.15),
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: AppColors.cardLight,
        selectedItemColor: AppColors.primaryViolet,
        unselectedItemColor: AppColors.textMutedLight,
      ),
    );
  }

  static TextTheme _buildTextTheme(Color baseColor) {
    return TextTheme(
      displayLarge: GoogleFonts.inter(
          fontSize: 57, fontWeight: FontWeight.w700, color: baseColor),
      displayMedium: GoogleFonts.inter(
          fontSize: 45, fontWeight: FontWeight.w700, color: baseColor),
      displaySmall: GoogleFonts.inter(
          fontSize: 36, fontWeight: FontWeight.w600, color: baseColor),
      headlineLarge: GoogleFonts.inter(
          fontSize: 32, fontWeight: FontWeight.w600, color: baseColor),
      headlineMedium: GoogleFonts.inter(
          fontSize: 28, fontWeight: FontWeight.w600, color: baseColor),
      headlineSmall: GoogleFonts.inter(
          fontSize: 24, fontWeight: FontWeight.w600, color: baseColor),
      titleLarge: GoogleFonts.inter(
          fontSize: 22, fontWeight: FontWeight.w600, color: baseColor),
      titleMedium: GoogleFonts.inter(
          fontSize: 16, fontWeight: FontWeight.w600, color: baseColor),
      titleSmall: GoogleFonts.inter(
          fontSize: 14, fontWeight: FontWeight.w500, color: baseColor),
      bodyLarge: GoogleFonts.inter(
          fontSize: 16, fontWeight: FontWeight.w400, color: baseColor),
      bodyMedium: GoogleFonts.inter(
          fontSize: 14, fontWeight: FontWeight.w400, color: baseColor),
      bodySmall: GoogleFonts.inter(
          fontSize: 12,
          fontWeight: FontWeight.w400,
          color: baseColor.withOpacity(0.7)),
      labelLarge: GoogleFonts.inter(
          fontSize: 14, fontWeight: FontWeight.w600, color: baseColor),
      labelMedium: GoogleFonts.inter(
          fontSize: 12, fontWeight: FontWeight.w500, color: baseColor),
      labelSmall: GoogleFonts.inter(
          fontSize: 11,
          fontWeight: FontWeight.w500,
          color: baseColor.withOpacity(0.7)),
    );
  }

  static AppBarTheme _appBarTheme(ColorScheme cs, Color bg) => AppBarTheme(
        backgroundColor: bg,
        foregroundColor: cs.onSurface,
        elevation: 0,
        scrolledUnderElevation: 1,
        centerTitle: false,
        titleTextStyle: GoogleFonts.inter(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: cs.onSurface,
        ),
      );

  static CardTheme _cardTheme(Color bg) => CardTheme(
        color: bg,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        clipBehavior: Clip.antiAlias,
      );

  static InputDecorationTheme _inputTheme(
      ColorScheme cs, Brightness brightness) {
    final borderColor = brightness == Brightness.dark
        ? AppColors.textMutedDark.withOpacity(0.3)
        : AppColors.textMutedLight.withOpacity(0.3);
    return InputDecorationTheme(
      filled: true,
      fillColor: brightness == Brightness.dark
          ? AppColors.surfaceDark3
          : AppColors.surfaceLight2,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: borderColor),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: borderColor),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: cs.primary, width: 1.5),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: cs.error),
      ),
      labelStyle: GoogleFonts.inter(fontSize: 14),
      hintStyle: GoogleFonts.inter(fontSize: 14, color: cs.onSurfaceVariant),
    );
  }

  static ElevatedButtonThemeData _elevatedButtonTheme(ColorScheme cs) =>
      ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: cs.primary,
          foregroundColor: cs.onPrimary,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          textStyle:
              GoogleFonts.inter(fontSize: 15, fontWeight: FontWeight.w600),
        ),
      );

  static OutlinedButtonThemeData _outlinedButtonTheme(ColorScheme cs) =>
      OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: cs.primary,
          side: BorderSide(color: cs.primary),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          textStyle:
              GoogleFonts.inter(fontSize: 15, fontWeight: FontWeight.w600),
        ),
      );

  static TextButtonThemeData _textButtonTheme(ColorScheme cs) =>
      TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: cs.primary,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          textStyle:
              GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600),
        ),
      );

  static ChipThemeData _chipTheme(ColorScheme cs) => ChipThemeData(
        backgroundColor: cs.surfaceContainerHighest,
        labelStyle:
            GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w500),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        side: BorderSide.none,
      );
}
