import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../router/app_router.dart';

/// Shell scaffold used by all main application screens.
/// Provides bottom navigation and consistent app bar.
class BaseScreen extends StatelessWidget {
  final Widget child;

  const BaseScreen({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: child,
        ),
      ),
      bottomNavigationBar: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: _LifeGpsBottomNav(),
        ),
      ),
    );
  }
}

class _LifeGpsBottomNav extends StatelessWidget {
  static const _items = [
    (
      label: 'Dashboard',
      icon: Icons.dashboard_rounded,
      route: AppRoutes.dashboard
    ),
    (
      label: 'Missions',
      icon: Icons.rocket_launch_rounded,
      route: AppRoutes.missions
    ),
    (
      label: 'Planner',
      icon: Icons.calendar_today_rounded,
      route: AppRoutes.planner
    ),
    (
      label: 'Curator',
      icon: Icons.auto_stories_rounded,
      route: AppRoutes.curator
    ),
    (label: 'Profile', icon: Icons.person_rounded, route: AppRoutes.profile),
  ];

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    final cs = Theme.of(context).colorScheme;

    return NavigationBar(
      selectedIndex: _selectedIndex(location),
      onDestinationSelected: (i) => context.go(_items[i].route),
      backgroundColor: cs.surface,
      indicatorColor: cs.primary.withOpacity(0.15),
      destinations: _items
          .map((item) => NavigationDestination(
                icon: Icon(item.icon),
                label: item.label,
              ))
          .toList(),
    );
  }

  int _selectedIndex(String location) {
    for (var i = 0; i < _items.length; i++) {
      if (location.startsWith(_items[i].route)) return i;
    }
    return 0;
  }
}
