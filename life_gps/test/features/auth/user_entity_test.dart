import 'package:flutter_test/flutter_test.dart';
import 'package:life_gps/features/auth/domain/entities/user_entity.dart';

void main() {
  group('UserEntity', () {
    final testJson = {
      'id': '123e4567-e89b-12d3-a456-426614174000',
      'email': 'kalani@lifegps.com',
      'full_name': 'Kalani Mano',
      'archetype': 'Architect',
      'created_at': '2026-08-01T09:00:00Z',
    };

    test('parses from JSON correctly', () {
      final user = UserEntity.fromJson(testJson);
      expect(user.id, '123e4567-e89b-12d3-a456-426614174000');
      expect(user.email, 'kalani@lifegps.com');
      expect(user.fullName, 'Kalani Mano');
      expect(user.archetype, 'Architect');
    });

    test('displayName returns fullName when available', () {
      final user = UserEntity.fromJson(testJson);
      expect(user.displayName, 'Kalani Mano');
    });

    test('displayName falls back to email prefix', () {
      final user = UserEntity.fromJson({...testJson, 'full_name': null});
      expect(user.displayName, 'kalani');
    });

    test('initials are correct for two-word name', () {
      final user = UserEntity.fromJson(testJson);
      expect(user.initials, 'KM');
    });

    test('initials for single word name', () {
      final user = UserEntity.fromJson({...testJson, 'full_name': 'Kalani'});
      expect(user.initials, 'K');
    });
  });
}
