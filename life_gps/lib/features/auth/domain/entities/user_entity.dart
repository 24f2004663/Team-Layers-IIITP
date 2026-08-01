/// Domain entity representing an authenticated user.
class UserEntity {
  final String id;
  final String email;
  final String? fullName;
  final String? archetype;
  final DateTime createdAt;

  const UserEntity({
    required this.id,
    required this.email,
    this.fullName,
    this.archetype,
    required this.createdAt,
  });

  factory UserEntity.fromJson(Map<String, dynamic> json) => UserEntity(
        id: json['id']?.toString() ?? '',
        email: json['email'] as String? ?? '',
        fullName: json['full_name'] as String?,
        archetype: json['archetype'] as String?,
        createdAt: json['created_at'] != null
            ? DateTime.tryParse(json['created_at'] as String) ?? DateTime.now()
            : DateTime.now(),
      );

  String get displayName => fullName ?? email.split('@').first;
  String get initials {
    if (fullName == null || fullName!.isEmpty) return email[0].toUpperCase();
    final parts = fullName!.trim().split(' ');
    if (parts.length == 1) return parts[0][0].toUpperCase();
    return '${parts[0][0]}${parts.last[0]}'.toUpperCase();
  }
}
