import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

/// User avatar showing cached network image or fallback initials circle.
class AvatarWidget extends StatelessWidget {
  final String? imageUrl;
  final String? name;
  final double radius;

  const AvatarWidget({
    super.key,
    this.imageUrl,
    this.name,
    this.radius = 24,
  });

  @override
  Widget build(BuildContext context) {
    if (imageUrl != null && imageUrl!.isNotEmpty) {
      return CircleAvatar(
        radius: radius,
        backgroundImage: NetworkImage(imageUrl!),
        backgroundColor: AppColors.primaryViolet.withOpacity(0.2),
        onBackgroundImageError: (_, __) {},
      );
    }
    return CircleAvatar(
      radius: radius,
      backgroundColor: AppColors.primaryViolet,
      child: Text(
        _initials,
        style: TextStyle(
          color: Colors.white,
          fontSize: radius * 0.7,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }

  String get _initials {
    if (name == null || name!.isEmpty) return '?';
    final parts = name!.trim().split(' ');
    if (parts.length == 1) return parts[0][0].toUpperCase();
    return '${parts[0][0]}${parts.last[0]}'.toUpperCase();
  }
}
