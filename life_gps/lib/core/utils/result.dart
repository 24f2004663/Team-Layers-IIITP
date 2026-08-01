import 'package:flutter/foundation.dart';

@immutable
sealed class Failure {
  final String message;
  const Failure(this.message);

  @override
  String toString() => '$runtimeType: $message';
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No network connection.']);
}

class AuthFailure extends Failure {
  const AuthFailure(
      [super.message = 'Authentication failed. Please log in again.']);
}

class ValidationFailure extends Failure {
  final Map<String, List<String>>? errors;
  const ValidationFailure({String message = 'Invalid input data.', this.errors})
      : super(message);
}

class ServerFailure extends Failure {
  final int? statusCode;
  const ServerFailure(
      {String message = 'An error occurred on the server.', this.statusCode})
      : super(message);
}

class CacheFailure extends Failure {
  const CacheFailure([super.message = 'Failed to read/write local cache.']);
}

class UnknownFailure extends Failure {
  const UnknownFailure([super.message = 'An unexpected error occurred.']);
}

@immutable
sealed class Result<T> {
  const Result();

  const factory Result.success(T value) = Success<T>;
  const factory Result.failure(Failure failure) = FailureResult<T>;

  bool get isSuccess => this is Success<T>;
  bool get isFailure => this is FailureResult<T>;

  T? get valueOrNull => switch (this) {
        Success<T>(:final value) => value,
        _ => null,
      };

  Failure? get failureOrNull => switch (this) {
        FailureResult<T>(:final failure) => failure,
        _ => null,
      };

  R fold<R>({
    required R Function(T value) onSuccess,
    required R Function(Failure failure) onFailure,
  }) =>
      switch (this) {
        Success<T>(:final value) => onSuccess(value),
        FailureResult<T>(:final failure) => onFailure(failure),
      };
}

class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);

  @override
  bool operator ==(Object other) =>
      identical(this, other) || (other is Success<T> && other.value == value);

  @override
  int get hashCode => value.hashCode;
}

class FailureResult<T> extends Result<T> {
  final Failure failure;
  const FailureResult(this.failure);

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is FailureResult<T> && other.failure == failure);

  @override
  int get hashCode => failure.hashCode;
}
