import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/auth_service.dart';
import '../models/user.dart' as app_user;

// Estados
abstract class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object?> get props => [];
}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthAuthenticated extends AuthState {
  final User firebaseUser;
  final app_user.User? userData;

  const AuthAuthenticated({
    required this.firebaseUser,
    this.userData,
  });

  @override
  List<Object?> get props => [firebaseUser, userData];
}

class AuthUnauthenticated extends AuthState {}

class AuthError extends AuthState {
  final String message;

  const AuthError(this.message);

  @override
  List<Object> get props => [message];
}

// Eventos
abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object> get props => [];
}

class AuthStarted extends AuthEvent {}

class AuthRegisterRequested extends AuthEvent {
  final String email;
  final String password;

  const AuthRegisterRequested({
    required this.email,
    required this.password,
  });

  @override
  List<Object> get props => [email, password];
}

class AuthLoginRequested extends AuthEvent {
  final String email;
  final String password;

  const AuthLoginRequested({
    required this.email,
    required this.password,
  });

  @override
  List<Object> get props => [email, password];
}

class AuthLogoutRequested extends AuthEvent {}

class AuthUserChanged extends AuthEvent {
  final User? user;

  const AuthUserChanged(this.user);

  @override
  List<Object> get props => [user ?? 'null'];
}

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthService _authService;

  AuthBloc({required AuthService authService})
      : _authService = authService,
        super(AuthInitial()) {
    // Escuchar cambios en el estado de autenticación
    _authService.authStateChanges.listen((user) {
      add(AuthUserChanged(user));
    });

    on<AuthStarted>(_onAuthStarted);
    on<AuthRegisterRequested>(_onAuthRegisterRequested);
    on<AuthLoginRequested>(_onAuthLoginRequested);
    on<AuthLogoutRequested>(_onAuthLogoutRequested);
    on<AuthUserChanged>(_onAuthUserChanged);
  }

  void _onAuthStarted(AuthStarted event, Emitter<AuthState> emit) {
    final user = _authService.currentUser;
    if (user != null) {
      emit(AuthAuthenticated(firebaseUser: user));
    } else {
      emit(AuthUnauthenticated());
    }
  }

  Future<void> _onAuthRegisterRequested(
    AuthRegisterRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    final result = await _authService.registerWithEmailAndPassword(
      email: event.email,
      password: event.password,
    );

    if (result.success && result.user != null) {
      // El estado se actualizará automáticamente por AuthUserChanged
      // No emitimos aquí para evitar duplicados
    } else {
      emit(AuthError(result.error ?? 'Error desconocido'));
    }
  }

  Future<void> _onAuthLoginRequested(
    AuthLoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    final result = await _authService.signInWithEmailAndPassword(
      email: event.email,
      password: event.password,
    );

    if (result.success && result.user != null) {
      // El estado se actualizará automáticamente por AuthUserChanged
      // No emitimos aquí para evitar duplicados
    } else {
      emit(AuthError(result.error ?? 'Error desconocido'));
    }
  }

  Future<void> _onAuthLogoutRequested(
    AuthLogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    await _authService.signOut();
    // El estado se actualizará automáticamente por AuthUserChanged
  }

  Future<void> _onAuthUserChanged(
    AuthUserChanged event,
    Emitter<AuthState> emit,
  ) async {
    if (event.user != null) {
      // Obtener datos adicionales del usuario
      final userData = await _authService.getUserData(event.user!.uid);
      emit(AuthAuthenticated(
        firebaseUser: event.user!,
        userData: userData,
      ));
    } else {
      emit(AuthUnauthenticated());
    }
  }
}
