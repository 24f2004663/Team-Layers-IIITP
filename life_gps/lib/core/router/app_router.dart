import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../di/providers.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/screens/register_screen.dart';
import '../../features/onboarding/presentation/screens/onboarding_screen.dart';
import '../../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../../features/identity/presentation/screens/identity_screen.dart';
import '../../features/behavior/presentation/screens/behavior_screen.dart';
import '../../features/planner/presentation/screens/planner_screen.dart';
import '../../features/missions/presentation/screens/missions_screen.dart';
import '../../features/curator/presentation/screens/curator_screen.dart';
import '../../features/learning/presentation/screens/learning_screen.dart';
import '../../features/profile/presentation/screens/profile_screen.dart';
import '../../features/settings/presentation/screens/settings_screen.dart';
import '../widgets/base_screen.dart';

/// All named routes in the application.
class AppRoutes {
  static const splash = '/';
  static const login = '/login';
  static const register = '/register';
  static const onboarding = '/onboarding';
  static const dashboard = '/dashboard';
  static const identity = '/identity';
  static const behavior = '/behavior';
  static const gapAnalysis = '/gap-analysis';
  static const planner = '/planner';
  static const missions = '/missions';
  static const curator = '/curator';
  static const learning = '/learning';
  static const profile = '/profile';
  static const settings = '/settings';
}

/// GoRouter factory — reads auth state from Riverpod provider.
GoRouter buildRouter(WidgetRef ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: AppRoutes.splash,
    debugLogDiagnostics: true,
    redirect: (context, state) async {
      final isAuthenticated = authState.valueOrNull ?? false;
      final isPublicRoute = state.matchedLocation == AppRoutes.login ||
          state.matchedLocation == AppRoutes.register ||
          state.matchedLocation == AppRoutes.splash;

      if (!isAuthenticated && !isPublicRoute) {
        return AppRoutes.login;
      }
      if (isAuthenticated && state.matchedLocation == AppRoutes.login) {
        return AppRoutes.dashboard;
      }
      return null;
    },
    routes: [
      // ─── Splash ──────────────────────────────────────────────────────────
      GoRoute(
        path: AppRoutes.splash,
        pageBuilder: (context, state) => _fade(state, const _SplashPage()),
      ),

      // ─── Auth ─────────────────────────────────────────────────────────────
      GoRoute(
        path: AppRoutes.login,
        pageBuilder: (context, state) => _fade(state, const LoginScreen()),
      ),
      GoRoute(
        path: AppRoutes.register,
        pageBuilder: (context, state) => _fade(state, const RegisterScreen()),
      ),
      GoRoute(
        path: AppRoutes.onboarding,
        pageBuilder: (context, state) => _fade(state, const OnboardingScreen()),
      ),

      // ─── Main Shell ───────────────────────────────────────────────────────
      ShellRoute(
        builder: (context, state, child) => BaseScreen(child: child),
        routes: [
          GoRoute(
            path: AppRoutes.dashboard,
            pageBuilder: (context, state) =>
                _fade(state, const DashboardScreen()),
          ),
          GoRoute(
            path: AppRoutes.identity,
            pageBuilder: (context, state) =>
                _fade(state, const IdentityScreen()),
          ),
          GoRoute(
            path: AppRoutes.behavior,
            pageBuilder: (context, state) =>
                _fade(state, const BehaviorScreen()),
          ),
          GoRoute(
            path: AppRoutes.planner,
            pageBuilder: (context, state) =>
                _fade(state, const PlannerScreen()),
          ),
          GoRoute(
            path: AppRoutes.missions,
            pageBuilder: (context, state) =>
                _fade(state, const MissionsScreen()),
          ),
          GoRoute(
            path: AppRoutes.curator,
            pageBuilder: (context, state) =>
                _fade(state, const CuratorScreen()),
          ),
          GoRoute(
            path: AppRoutes.learning,
            pageBuilder: (context, state) =>
                _fade(state, const LearningScreen()),
          ),
          GoRoute(
            path: AppRoutes.profile,
            pageBuilder: (context, state) =>
                _fade(state, const ProfileScreen()),
          ),
          GoRoute(
            path: AppRoutes.settings,
            pageBuilder: (context, state) =>
                _fade(state, const SettingsScreen()),
          ),
        ],
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Page not found: ${state.error}'),
      ),
    ),
  );
}

CustomTransitionPage<void> _fade(GoRouterState state, Widget child) =>
    CustomTransitionPage<void>(
      key: state.pageKey,
      child: child,
      transitionDuration: const Duration(milliseconds: 250),
      transitionsBuilder: (context, animation, _, child) =>
          FadeTransition(opacity: animation, child: child),
    );

/// Internal splash that auto-redirects via GoRouter redirect logic.
class _SplashPage extends StatefulWidget {
  const _SplashPage();

  @override
  State<_SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<_SplashPage> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) context.go(AppRoutes.dashboard);
    });
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      backgroundColor: cs.surface,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.navigation_rounded, size: 72, color: cs.primary),
            const SizedBox(height: 24),
            Text(
              'Life-GPS',
              style: Theme.of(context)
                  .textTheme
                  .displaySmall
                  ?.copyWith(color: cs.primary),
            ),
            const SizedBox(height: 8),
            Text(
              'Your AI Life Operating System',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: cs.onSurfaceVariant,
                  ),
            ),
            const SizedBox(height: 48),
            CircularProgressIndicator(color: cs.primary),
          ],
        ),
      ),
    );
  }
}
