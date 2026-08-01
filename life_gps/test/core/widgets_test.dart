import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:life_gps/core/widgets/app_button.dart';
import 'package:life_gps/core/widgets/error_state_widget.dart';
import 'package:life_gps/core/widgets/empty_state_widget.dart';
import 'package:life_gps/core/widgets/progress_card.dart';
import 'package:life_gps/core/widgets/avatar_widget.dart';
import 'package:life_gps/core/theme/app_theme.dart';

Widget _wrap(Widget child) => MaterialApp(
      theme: AppTheme.dark,
      home: Scaffold(body: child),
    );

void main() {
  group('AppButton', () {
    testWidgets('renders label', (tester) async {
      await tester.pumpWidget(_wrap(
        AppButton(label: 'Test Button', onPressed: () {}),
      ));
      expect(find.text('Test Button'), findsOneWidget);
    });

    testWidgets('shows loading spinner when isLoading', (tester) async {
      await tester.pumpWidget(_wrap(
        const AppButton(label: 'Loading', isLoading: true),
      ));
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('is disabled when onPressed is null', (tester) async {
      await tester.pumpWidget(_wrap(
        const AppButton(label: 'Disabled'),
      ));
      final btn = tester.widget<FilledButton>(find.byType(FilledButton));
      expect(btn.onPressed, isNull);
    });
  });

  group('ErrorStateWidget', () {
    testWidgets('renders message', (tester) async {
      await tester.pumpWidget(_wrap(
        const ErrorStateWidget(message: 'Something failed'),
      ));
      expect(find.text('Something failed'), findsOneWidget);
    });

    testWidgets('shows retry button when onRetry provided', (tester) async {
      var tapped = false;
      await tester.pumpWidget(_wrap(
        ErrorStateWidget(message: 'Error', onRetry: () => tapped = true),
      ));
      await tester.tap(find.text('Try Again'));
      expect(tapped, isTrue);
    });
  });

  group('EmptyStateWidget', () {
    testWidgets('renders title and subtitle', (tester) async {
      await tester.pumpWidget(_wrap(
        const EmptyStateWidget(
            title: 'Nothing here', subtitle: 'Add something'),
      ));
      expect(find.text('Nothing here'), findsOneWidget);
      expect(find.text('Add something'), findsOneWidget);
    });
  });

  group('ProgressCard', () {
    testWidgets('renders title and correct percentage', (tester) async {
      await tester.pumpWidget(_wrap(
        const ProgressCard(title: 'Missions', progress: 0.75),
      ));
      expect(find.text('Missions'), findsOneWidget);
      expect(find.text('75%'), findsOneWidget);
    });
  });

  group('AvatarWidget', () {
    testWidgets('shows initials when no imageUrl', (tester) async {
      await tester.pumpWidget(_wrap(
        const AvatarWidget(name: 'Kalani Mano'),
      ));
      expect(find.text('KM'), findsOneWidget);
    });

    testWidgets('shows ? for empty name', (tester) async {
      await tester.pumpWidget(_wrap(const AvatarWidget()));
      expect(find.text('?'), findsOneWidget);
    });
  });
}
