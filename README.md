# Revenue Recovery SaaS

Plataforma SaaS para automatizar la recuperación de ingresos perdidos por pagos fallidos.

## 🎯 Objetivo

Ayudar a empresas SaaS B2B a recuperar 15-40% de pagos fallidos mediante campañas automatizadas inteligentes.

## 🏗️ Arquitectura

- **Frontend**: Flutter Web + Firebase
- **Backend**: Cloud Functions + Firestore  
- **Hosting**: Firebase Hosting
- **Auth**: Firebase Authentication

## ⚡ Quick Start

### Setup Automático (Recomendado)

```bash
# Setup completo automatizado
python scripts/setup_improved.py

# Validar configuración
python scripts/validate_setup_improved.py

# Iniciar desarrollo
python scripts/dev.py
```

### Helpers Multiplataforma

```bash
# Windows
.\run.bat setup      # Setup automático
.\run.bat validate   # Validar entorno
.\run.bat dev        # Desarrollo local

# macOS/Linux
./run.sh setup       # Setup automático
./run.sh validate    # Validar entorno
./run.sh dev         # Desarrollo local
```

## 📋 Requisitos

### Sistema
- **Python 3.7+** - Scripts de automatización
- **Flutter SDK** - Desarrollo frontend
- **Node.js 16+** - Firebase Functions
- **Firebase CLI** - Deploy y desarrollo

### Auto-instalación
El script `setup_improved.py` puede instalar automáticamente:
- ✅ Node.js (Windows/macOS/Linux)
- ✅ Firebase CLI via npm
- ✅ FlutterFire CLI via dart pub
- ✅ Dependencias del proyecto

## 🚀 Desarrollo

### Configuración Initial

```bash
# 1. Setup automatizado
python scripts/setup_improved.py

# 2. Configurar Firebase (manual)
cd backend
firebase init

# 3. Configurar FlutterFire
cd ../frontend
flutterfire configure --project=tu-proyecto

# 4. Iniciar desarrollo
python scripts/dev.py
```

### Comandos Disponibles

| Comando | Descripción | Windows | Unix/macOS |
|---------|-------------|---------|------------|
| **Setup** | Configuración automática | `python scripts\setup_improved.py` | `python3 scripts/setup_improved.py` |
| **Validación** | Verificar entorno | `python scripts\validate_setup_improved.py` | `python3 scripts/validate_setup_improved.py` |
| **Desarrollo** | Servidor local | `python scripts\dev.py` | `python3 scripts/dev.py` |
| **Testing** | Tests automatizados | `python scripts\test.py` | `python3 scripts/test.py` |
| **Deploy** | Deploy producción | `python scripts\deploy.py` | `python3 scripts/deploy.py` |

### URLs de Desarrollo

- **App Principal:** http://localhost:3000
- **Firebase Emulator UI:** http://localhost:4000  
- **Functions API:** http://localhost:5001
- **Firestore:** http://localhost:8080

# Deploy a producción
python scripts/deploy.py
```

### URLs de Desarrollo

- **Flutter Web**: http://localhost:3000
- **Firebase Emulator UI**: http://localhost:4000
- **Firestore Emulator**: http://localhost:8080
- **Functions Emulator**: http://localhost:5001

## 🏃‍♂️ Sprint Actual

### Sprint 1: Fundación del Proyecto ✅

**Historia 1.1: Registro de Usuario** - ✅ COMPLETADA
- [x] Pantalla de registro con validaciones
- [x] Integración Firebase Auth  
- [x] Creación automática de perfil
- [x] Manejo de errores
- [x] Redirección automática

**Historia 1.2: Login de Usuario** - 🚧 EN PROGRESO

## 📂 Estructura del Proyecto

```
revenue_recovery_saas/
├── frontend/                    # Flutter Web App
│   ├── lib/
│   │   ├── models/             # Modelos de datos
│   │   ├── services/           # Servicios y BLoCs
│   │   ├── screens/            # Pantallas de la app
│   │   ├── widgets/            # Widgets reutilizables
│   │   └── main.dart           # Punto de entrada
│   ├── web/                    # Configuración web
│   └── pubspec.yaml            # Dependencias Flutter
├── backend/                     # Firebase Backend
│   ├── functions/              # Cloud Functions
│   ├── firebase.json           # Configuración Firebase
│   └── firestore.rules         # Reglas de seguridad
├── scripts/                     # Scripts de desarrollo
│   ├── setup.py               # Configuración inicial
│   ├── dev.py                 # Desarrollo local
│   ├── test.py                # Testing
│   └── deploy.py              # Deploy
├── docs/                       # Documentación
└── README.md                   # Este archivo
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python scripts/test.py

# Solo análisis estático
cd frontend && flutter analyze

# Solo tests unitarios  
cd frontend && flutter test
```

## 🚀 Deploy

```bash
# Deploy completo
python scripts/deploy.py

# Deploy individual
cd backend
firebase deploy --only functions
firebase deploy --only hosting
firebase deploy --only firestore:rules
```

## 📖 Documentación

- [PRD Completo](docs/revenue_recovery_prd.md)
- [Roadmap por Sprints](docs/sprint_roadmap.md)
- [Historias de Usuario Sprint 1](docs/sprint1_user_stories.md)
- [Setup Historia 1.1](docs/HISTORIA_1_1_SETUP.md)
- [Diagramas de Secuencia](docs/sprint1_sequence_diagrams.mermaid)

## 🎨 Stack Tecnológico

### Frontend
- **Flutter Web** - Framework de UI
- **Firebase Auth** - Autenticación
- **BLoC Pattern** - Gestión de estado
- **Go Router** - Navegación
- **Material Design** - Sistema de diseño

### Backend  
- **Cloud Functions** - Lógica de negocio
- **Firestore** - Base de datos NoSQL
- **Firebase Hosting** - Hosting estático
- **TypeScript** - Lenguaje de desarrollo

### DevOps
- **Python** - Scripts de automatización
- **Firebase CLI** - Despliegue
- **Git** - Control de versiones

## 🏆 Métricas Objetivo

- **Recovery Rate**: >25%
- **Time to First Recovery**: <24h
- **Customer Onboarding**: <30 min
- **Platform Uptime**: >99.9%

## 👥 Target

SaaS B2B con:
- $500K+ ARR
- 3-8% churn por problemas de facturación
- Equipos finance/ops 5-50 personas

## 📝 License

Propietario - Revenue Recovery SaaS

---

**Nota**: Este proyecto está en desarrollo activo. Sprint 1 en progreso.
