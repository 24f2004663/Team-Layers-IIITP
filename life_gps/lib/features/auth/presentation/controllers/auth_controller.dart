import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/errors/error_handler.dart';
import '../../../../core/services/auth_service.dart';
import '../../../../core/di/providers.dart';
import '../../domain/entities/user_entity.dart';

sealed class AuthState {
  const AuthState();
}

class AuthInitial extends AuthState {
  const AuthInitial();
}

class AuthLoading extends AuthState {
  const AuthLoading();
}

class AuthSuccess extends AuthState {
  final UserEntity user;
  const AuthSuccess(this.user);
}

class AuthError extends AuthState {
  final String message;
  final String? code;
  const AuthError({required this.message, this.code});
}

/// Riverpod notifier managing login, register, and logout state.
class AuthController extends Notifier<AuthState> {
  AuthService get _authService => ref.read(authServiceProvider);

  @override
  AuthState build() => const AuthInitial();

  Future<bool> login({required String email, required String password}) async {
    state = const AuthLoading();
    try {
      final user = await _authService.login(email: email, password: password);
      state = AuthSuccess(user);
      return true;
    } catch (e) {
      final exc = ErrorHandler.handle(e);
      state = AuthError(message: exc.message, code: exc.code);
      return false;
    }
  }

  Future<bool> register({
    required String email,
    required String password,
    required String fullName,
    String archetype = 'Explorer',
    List<String> coreValues = const [],
    List<String> strengths = const [],
    List<String> weaknesses = const [],
  }) async {
    state = const AuthLoading();
    try {
      final user = await _authService.register(
        email: email,
        password: password,
        fullName: fullName,
        archetype: archetype,
        coreValues: coreValues,
        strengths: strengths,
        weaknesses: weaknesses,
      );
      state = AuthSuccess(user);
      return true;
    } catch (e) {
      final exc = ErrorHandler.handle(e);
      state = AuthError(message: exc.message, code: exc.code);
      return false;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    state = const AuthInitial();
    ref.invalidate(authStateProvider);
  }
}

final authControllerProvider = NotifierProvider<AuthController, AuthState>(
  AuthController.new,
  name: 'authControllerProvider',
);
