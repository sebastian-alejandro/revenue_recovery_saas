# Scripts de Desarrollo - Historia 1.1

Scripts en Python para mayor compatibilidad multiplataforma.

## Requisitos
- Python 3.7+
- Flutter SDK
- Node.js
- Firebase CLI

## Uso

### Setup inicial
```bash
python scripts/setup.py
```

### Desarrollo
```bash
python scripts/dev.py
```

### Testing
```bash
python scripts/test.py
```

### Deploy
```bash
python scripts/deploy.py
```

## Scripts disponibles

### `setup.py`
- Verifica dependencias (Flutter, Node.js, Firebase CLI)
- Instala dependencias de Flutter y npm
- Valida estructura de archivos
- Configura el entorno de desarrollo

### `dev.py`
- Inicia Flutter Web en puerto 3000
- Inicia Firebase Emulators
- Monitorea servicios en tiempo real
- Manejo de Ctrl+C para detener servicios

### `test.py`
- Ejecuta análisis estático de Flutter
- Verifica formato de código
- Ejecuta tests unitarios
- Compila TypeScript Functions
- Genera reporte de resultados

### `deploy.py`
- Ejecuta tests pre-deploy
- Construye Flutter Web para producción
- Construye Cloud Functions
- Despliega reglas de Firestore
- Despliega Functions y Hosting
- Muestra URL de la aplicación

## Compatibilidad
- ✅ Windows (PowerShell, CMD)
- ✅ macOS (Terminal, Zsh, Bash)
- ✅ Linux (Bash, Zsh)

## Troubleshooting

### Error: Python no encontrado
```bash
# Windows
python --version
# Si no funciona, instalar desde python.org

# macOS
python3 --version
# Usar python3 en lugar de python

# Linux
python3 --version
sudo apt install python3
```

### Error: Firebase CLI no encontrado
```bash
npm install -g firebase-tools
```

### Error: Flutter no encontrado
- Instalar Flutter SDK desde https://flutter.dev
- Agregar Flutter al PATH del sistema
