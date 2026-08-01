// ─── Auth DTOs ────────────────────────────────────────────────────────────────

class TokenResponseDto {
  final String accessToken;
  final String tokenType;

  const TokenResponseDto({required this.accessToken, required this.tokenType});

  factory TokenResponseDto.fromJson(Map<String, dynamic> json) =>
      TokenResponseDto(
        accessToken: json['access_token'] as String,
        tokenType: json['token_type'] as String? ?? 'bearer',
      );
}

class LoginRequestDto {
  final String email;
  final String password;

  const LoginRequestDto({required this.email, required this.password});

  Map<String, dynamic> toFormData() =>
      {'username': email, 'password': password};
}

class RegisterRequestDto {
  final String email;
  final String password;
  final String fullName;
  final String archetype;
  final List<String> coreValues;
  final List<String> strengths;
  final List<String> weaknesses;

  const RegisterRequestDto({
    required this.email,
    required this.password,
    required this.fullName,
    this.archetype = 'Explorer',
    this.coreValues = const [],
    this.strengths = const [],
    this.weaknesses = const [],
  });

  Map<String, dynamic> toJson() => {
        'email': email,
        'password': password,
        'full_name': fullName,
        'archetype': archetype,
        'core_values': coreValues,
        'strengths': strengths,
        'weaknesses': weaknesses,
      };
}
