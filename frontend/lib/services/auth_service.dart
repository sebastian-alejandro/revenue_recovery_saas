import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:cloud_functions/cloud_functions.dart';
import 'package:logger/logger.dart';
import '../models/user.dart' as app_user;

class AuthService {
  final firebase_auth.FirebaseAuth _firebaseAuth;
  final FirebaseFirestore _firestore;
  final FirebaseFunctions _functions;
  final Logger _logger;

  AuthService({
    firebase_auth.FirebaseAuth? firebaseAuth,
    FirebaseFirestore? firestore,
    FirebaseFunctions? functions,
    Logger? logger,
  })  : _firebaseAuth = firebaseAuth ?? firebase_auth.FirebaseAuth.instance,
        _firestore = firestore ?? FirebaseFirestore.instance,
        _functions = functions ?? FirebaseFunctions.instance,
        _logger = logger ?? Logger();

  // Stream del usuario actual
  Stream<firebase_auth.User?> get authStateChanges =>
      _firebaseAuth.authStateChanges();

  // Usuario actual
  firebase_auth.User? get currentUser => _firebaseAuth.currentUser;

  // Registro de usuario
  Future<AuthResult> registerWithEmailAndPassword({
    required String email,
    required String password,
  }) async {
    try {
      _logger.i('Iniciando registro para: $email');

      // Crear usuario en Firebase Auth
      final credential = await _firebaseAuth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      final user = credential.user;
      if (user == null) {
        throw Exception('No se pudo crear el usuario');
      }

      _logger.i('Usuario creado en Firebase Auth: ${user.uid}');

      // Crear perfil de usuario usando Cloud Function
      final createProfileFunction =
          _functions.httpsCallable('createUserProfile');
      final result = await createProfileFunction.call({
        'userId': user.uid,
        'email': email,
      });

      _logger.i('Perfil de usuario creado: ${result.data}');

      return AuthResult.success(user);
    } on firebase_auth.FirebaseAuthException catch (e) {
      _logger.e('Error de Firebase Auth: ${e.code} - ${e.message}');
      return AuthResult.error(_mapFirebaseError(e.code));
    } catch (e) {
      _logger.e('Error inesperado en registro: $e');
      return AuthResult.error(
          'Ocurrió un error inesperado. Inténtalo de nuevo.');
    }
  }

  // Login de usuario
  Future<AuthResult> signInWithEmailAndPassword({
    required String email,
    required String password,
  }) async {
    try {
      _logger.i('Iniciando login para: $email');

      final credential = await _firebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      final user = credential.user;
      if (user == null) {
        throw Exception('No se pudo autenticar el usuario');
      }

      _logger.i('Usuario autenticado: ${user.uid}');

      // Obtener datos del perfil usando Cloud Function
      final getUserProfileFunction = _functions.httpsCallable('getUserProfile');
      final result = await getUserProfileFunction.call({
        'userId': user.uid,
      });

      _logger.i('Perfil de usuario obtenido: ${result.data}');

      return AuthResult.success(user);
    } on firebase_auth.FirebaseAuthException catch (e) {
      _logger.e('Error de Firebase Auth: ${e.code} - ${e.message}');
      return AuthResult.error(_mapFirebaseError(e.code));
    } catch (e) {
      _logger.e('Error inesperado en login: $e');
      return AuthResult.error(
          'Ocurrió un error inesperado. Inténtalo de nuevo.');
    }
  }

  // Logout
  Future<void> signOut() async {
    try {
      _logger.i('Cerrando sesión');
      await _firebaseAuth.signOut();
    } catch (e) {
      _logger.e('Error al cerrar sesión: $e');
      rethrow;
    }
  }

  // Obtener datos del usuario de Firestore
  Future<app_user.User?> getUserData(String userId) async {
    try {
      final doc = await _firestore.collection('users').doc(userId).get();

      if (!doc.exists) {
        return null;
      }

      return app_user.User.fromJson({
        'id': doc.id,
        ...doc.data()!,
      });
    } catch (e) {
      _logger.e('Error al obtener datos del usuario: $e');
      return null;
    }
  }

  // Mapear errores de Firebase a mensajes amigables
  String _mapFirebaseError(String code) {
    switch (code) {
      case 'weak-password':
        return 'La contraseña es muy débil. Debe tener al menos 8 caracteres.';
      case 'email-already-in-use':
        return 'Ya existe una cuenta con este email.';
      case 'invalid-email':
        return 'El formato del email no es válido.';
      case 'user-not-found':
        return 'No existe una cuenta con este email.';
      case 'wrong-password':
        return 'La contraseña es incorrecta.';
      case 'too-many-requests':
        return 'Demasiados intentos fallidos. Inténtalo más tarde.';
      case 'network-request-failed':
        return 'Error de conexión. Verifica tu internet.';
      default:
        return 'Ocurrió un error. Inténtalo de nuevo.';
    }
  }
}

// Clase para el resultado de autenticación
class AuthResult {
  final bool success;
  final firebase_auth.User? user;
  final String? error;

  AuthResult.success(this.user)
      : success = true,
        error = null;

  AuthResult.error(this.error)
      : success = false,
        user = null;
}
