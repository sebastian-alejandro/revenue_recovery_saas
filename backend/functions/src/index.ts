import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

// Inicializar Firebase Admin
admin.initializeApp();

const db = admin.firestore();

// Cloud Function para crear perfil de usuario
export const createUserProfile = functions.https.onCall(async (data, context) => {
  // Verificar autenticación
  if (!context.auth) {
    throw new functions.https.HttpsError(
      'unauthenticated',
      'El usuario debe estar autenticado.'
    );
  }

  const { userId, email } = data;

  // Validar datos requeridos
  if (!userId || !email) {
    throw new functions.https.HttpsError(
      'invalid-argument',
      'userId y email son requeridos.'
    );
  }

  // Verificar que el UID coincida con el usuario autenticado
  if (context.auth.uid !== userId) {
    throw new functions.https.HttpsError(
      'permission-denied',
      'No tienes permisos para crear este perfil.'
    );
  }

  try {
    const now = admin.firestore.Timestamp.now();
    
    // Crear documento del usuario
    const userDoc = {
      id: userId,
      email: email,
      displayName: null,
      companyId: null,
      createdAt: now,
      updatedAt: now,
      metadata: {
        onboardingCompleted: false,
        emailVerified: context.auth.token.email_verified || false,
      }
    };

    // Guardar en Firestore
    await db.collection('users').doc(userId).set(userDoc);

    functions.logger.info(`Perfil de usuario creado: ${userId}`, { email });

    return {
      success: true,
      message: 'Perfil de usuario creado exitosamente',
      userId: userId
    };

  } catch (error) {
    functions.logger.error('Error al crear perfil de usuario:', error);
    throw new functions.https.HttpsError(
      'internal',
      'Error interno del servidor'
    );
  }
});

// Cloud Function para obtener perfil de usuario
export const getUserProfile = functions.https.onCall(async (data, context) => {
  // Verificar autenticación
  if (!context.auth) {
    throw new functions.https.HttpsError(
      'unauthenticated',
      'El usuario debe estar autenticado.'
    );
  }

  const { userId } = data;

  // Usar el UID del usuario autenticado si no se proporciona userId
  const targetUserId = userId || context.auth.uid;

  // Verificar permisos - solo puede acceder a su propio perfil
  if (context.auth.uid !== targetUserId) {
    throw new functions.https.HttpsError(
      'permission-denied',
      'No tienes permisos para acceder a este perfil.'
    );
  }

  try {
    // Obtener documento del usuario
    const userDoc = await db.collection('users').doc(targetUserId).get();

    if (!userDoc.exists) {
      throw new functions.https.HttpsError(
        'not-found',
        'Perfil de usuario no encontrado.'
      );
    }

    const userData = userDoc.data();

    functions.logger.info(`Perfil de usuario obtenido: ${targetUserId}`);

    return {
      success: true,
      data: {
        ...userData,
        id: userDoc.id
      }
    };

  } catch (error) {
    functions.logger.error('Error al obtener perfil de usuario:', error);
    
    if (error instanceof functions.https.HttpsError) {
      throw error;
    }
    
    throw new functions.https.HttpsError(
      'internal',
      'Error interno del servidor'
    );
  }
});

// Cloud Function para obtener datos iniciales del dashboard
export const getInitialData = functions.https.onCall(async (data, context) => {
  // Verificar autenticación
  if (!context.auth) {
    throw new functions.https.HttpsError(
      'unauthenticated',
      'El usuario debe estar autenticado.'
    );
  }

  try {
    // Obtener perfil del usuario
    const userDoc = await db.collection('users').doc(context.auth.uid).get();

    if (!userDoc.exists) {
      throw new functions.https.HttpsError(
        'not-found',
        'Perfil de usuario no encontrado.'
      );
    }

    const userData = userDoc.data();
    const companyId = userData?.companyId;

    // Si no tiene empresa asociada, retornar estado de onboarding
    if (!companyId) {
      return {
        success: true,
        data: {
          hasCompany: false,
          needsOnboarding: true,
          user: userData
        }
      };
    }

    // Obtener datos básicos de la empresa y collections vacías
    const [companyDoc] = await Promise.all([
      db.collection('companies').doc(companyId).get()
    ]);

    const companyData = companyDoc.exists ? companyDoc.data() : null;

    return {
      success: true,
      data: {
        hasCompany: true,
        needsOnboarding: false,
        user: userData,
        company: companyData,
        // Placeholder data para dashboard vacío
        metrics: {
          totalRevenue: 0,
          recoveredRevenue: 0,
          recoveryRate: 0,
          activeCustomers: 0
        },
        recentActivity: []
      }
    };

  } catch (error) {
    functions.logger.error('Error al obtener datos iniciales:', error);
    
    if (error instanceof functions.https.HttpsError) {
      throw error;
    }
    
    throw new functions.https.HttpsError(
      'internal',
      'Error interno del servidor'
    );
  }
});
