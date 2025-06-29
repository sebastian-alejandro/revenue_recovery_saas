#!/usr/bin/env python3
"""
Setup Script Avanzado para Historia 1.1: Registro de Usuario
Versión mejorada con:
- Auto-detección de sistema operativo
- Configuración automática de Firebase
- Validación continua durante setup
- Recovery automático de errores
"""

import os
import sys
import json
import subprocess
import shutil
import platform
import urllib.request
from pathlib import Path
from typing import Tuple, Optional

def print_colored(message, color='white'):
    """Imprime mensaje con color en la terminal"""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['white'])}{message}{colors['reset']}")

def run_command(command, cwd=None, description="", timeout=120):
    """Ejecuta un comando con manejo de errores mejorado"""
    if description:
        print_colored(f"🔄 {description}...", 'yellow')
    
    try:
        # Usar shell apropiado para el sistema
        shell = True
        if platform.system() == "Windows":
            # En Windows, usar PowerShell para mejor compatibilidad
            if not command.startswith('powershell'):
                command = f'powershell -Command "{command}"'
        
        result = subprocess.run(
            command, 
            shell=shell, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            if description:
                print_colored(f"✅ {description} - Exitoso", 'green')
            return True, result.stdout, result.stderr
        else:
            if description:
                print_colored(f"❌ {description} - Falló", 'red')
            if result.stderr.strip():
                print_colored(f"   Error: {result.stderr.strip()}", 'red')
            return False, result.stdout, result.stderr
            
    except subprocess.TimeoutExpired:
        print_colored(f"❌ {description} - Timeout después de {timeout}s", 'red')
        return False, "", "Timeout"
    except Exception as e:
        if description:
            print_colored(f"❌ Error ejecutando {description}: {e}", 'red')
        return False, "", str(e)

def check_internet_connection():
    """Verifica conectividad a internet"""
    try:
        urllib.request.urlopen('http://google.com', timeout=10)
        return True
    except Exception:
        return False

def detect_system_info():
    """Detecta información del sistema"""
    system = platform.system()
    arch = platform.machine()
    version = platform.version()
    
    print_colored(f"🖥️ Sistema detectado: {system} {arch}", 'cyan')
    print_colored(f"📱 Versión: {version}", 'cyan')
    
    return {
        'system': system,
        'arch': arch,
        'version': version,
        'is_windows': system == "Windows",
        'is_macos': system == "Darwin",
        'is_linux': system == "Linux"
    }

def check_and_install_dependency(command, name, install_commands=None):
    """Verifica e instala dependencias automáticamente"""
    print_colored(f"🔍 Verificando {name}...", 'blue')
    
    # Verificar si ya está instalado
    cmd_check = command.split()[0]
    if shutil.which(cmd_check):
        success, stdout, stderr = run_command(f"{command} --version", timeout=30)
        if success:
            version = stdout.split('\n')[0] if stdout else "Unknown"
            print_colored(f"✅ {name} ya instalado: {version}", 'green')
            return True
    
    print_colored(f"⚠️ {name} no encontrado", 'yellow')
    
    if not install_commands:
        print_colored(f"❌ No hay comando de instalación automática para {name}", 'red')
        return False
    
    # Intentar instalación automática
    system_info = detect_system_info()
    
    for install_type, install_cmd in install_commands.items():
        if install_type == 'windows' and system_info['is_windows']:
            print_colored(f"🔄 Instalando {name} en Windows...", 'yellow')
            success, stdout, stderr = run_command(install_cmd, description=f"Instalando {name}")
            if success:
                return True
        elif install_type == 'macos' and system_info['is_macos']:
            print_colored(f"🔄 Instalando {name} en macOS...", 'yellow')
            success, stdout, stderr = run_command(install_cmd, description=f"Instalando {name}")
            if success:
                return True
        elif install_type == 'linux' and system_info['is_linux']:
            print_colored(f"🔄 Instalando {name} en Linux...", 'yellow')
            success, stdout, stderr = run_command(install_cmd, description=f"Instalando {name}")
            if success:
                return True
        elif install_type == 'universal':
            print_colored(f"🔄 Instalando {name} (universal)...", 'yellow')
            success, stdout, stderr = run_command(install_cmd, description=f"Instalando {name}")
            if success:
                return True
    
    print_colored(f"❌ No se pudo instalar {name} automáticamente", 'red')
    return False

def setup_system_dependencies():
    """Configura dependencias del sistema"""
    print_colored("🔧 Configurando dependencias del sistema...", 'cyan')
    
    if not check_internet_connection():
        print_colored("❌ Sin conexión a internet. Se requiere conectividad para el setup.", 'red')
        return False
    
    dependencies = {
        'Python': {
            'command': 'python',
            'install_commands': {
                'windows': 'winget install Python.Python.3',
                'macos': 'brew install python',
                'linux': 'sudo apt-get update && sudo apt-get install python3 python3-pip'
            }
        },
        'Node.js': {
            'command': 'node',
            'install_commands': {
                'windows': 'winget install OpenJS.NodeJS',
                'macos': 'brew install node',
                'linux': 'curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs'
            }
        },
        'Git': {
            'command': 'git',
            'install_commands': {
                'windows': 'winget install Git.Git',
                'macos': 'brew install git',
                'linux': 'sudo apt-get install git'
            }
        }
    }
    
    all_success = True
    for name, config in dependencies.items():
        success = check_and_install_dependency(
            config['command'], 
            name, 
            config.get('install_commands')
        )
        if not success:
            all_success = False
    
    return all_success

def setup_flutter():
    """Configura Flutter específicamente"""
    print_colored("📱 Configurando Flutter...", 'cyan')
    
    # Verificar si Flutter está instalado
    if not shutil.which('flutter'):
        print_colored("❌ Flutter no está instalado", 'red')
        print_colored("🔗 Instalar Flutter desde: https://flutter.dev/docs/get-started/install", 'yellow')
        return False
    
    # Verificar versión de Flutter
    success, stdout, stderr = run_command("flutter --version")
    if success:
        print_colored(f"✅ Flutter encontrado", 'green')
        
        # Mostrar información de Flutter
        lines = stdout.split('\n')
        for line in lines[:3]:  # Primeras 3 líneas tienen info importante
            if line.strip():
                print_colored(f"   {line.strip()}", 'white')
    
    # Habilitar web support
    success, stdout, stderr = run_command("flutter config --enable-web", 
                                         description="Habilitando Flutter Web")
    if not success:
        print_colored("⚠️ No se pudo habilitar Flutter Web automáticamente", 'yellow')
    
    # Verificar que web está habilitado
    success, stdout, stderr = run_command("flutter config")
    if success and "enable-web: true" in stdout:
        print_colored("✅ Flutter Web habilitado correctamente", 'green')
    else:
        print_colored("❌ Flutter Web no está habilitado", 'red')
        return False
    
    # Ejecutar flutter doctor
    print_colored("🩺 Ejecutando Flutter Doctor...", 'blue')
    success, stdout, stderr = run_command("flutter doctor", timeout=60)
    if success:
        # Contar problemas
        issues = stdout.count('✗')
        warnings = stdout.count('!')
        
        if issues == 0:
            print_colored("✅ Flutter Doctor: Sin problemas", 'green')
        else:
            print_colored(f"⚠️ Flutter Doctor: {issues} problemas, {warnings} warnings", 'yellow')
            
            # Mostrar primeros problemas
            lines = stdout.split('\n')
            problem_lines = [line for line in lines if '✗' in line or '!' in line]
            for line in problem_lines[:3]:  # Solo primeros 3 problemas
                print_colored(f"   {line.strip()}", 'yellow')
    
    return True

def setup_firebase_cli():
    """Configura Firebase CLI"""
    print_colored("🔥 Configurando Firebase CLI...", 'cyan')
    
    # Verificar si npm está disponible
    if not shutil.which('npm'):
        print_colored("❌ npm no está disponible. Instalar Node.js primero.", 'red')
        return False
    
    # Verificar si Firebase CLI ya está instalado
    if shutil.which('firebase'):
        success, stdout, stderr = run_command("firebase --version")
        if success:
            print_colored(f"✅ Firebase CLI ya instalado: {stdout.strip()}", 'green')
            return True
    
    # Instalar Firebase CLI
    print_colored("📦 Instalando Firebase CLI...", 'yellow')
    success, stdout, stderr = run_command("npm install -g firebase-tools", 
                                         description="Instalando Firebase CLI",
                                         timeout=180)
    
    if not success:
        print_colored("❌ Falló la instalación de Firebase CLI", 'red')
        print_colored("💡 Ejecutar manualmente: npm install -g firebase-tools", 'yellow')
        return False
    
    # Verificar instalación
    if shutil.which('firebase'):
        success, stdout, stderr = run_command("firebase --version")
        if success:
            print_colored(f"✅ Firebase CLI instalado exitosamente: {stdout.strip()}", 'green')
            return True
    
    print_colored("❌ Firebase CLI no se pudo verificar después de la instalación", 'red')
    return False

def setup_flutterfire_cli():
    """Configura FlutterFire CLI"""
    print_colored("🔥📱 Configurando FlutterFire CLI...", 'cyan')
    
    # Instalar FlutterFire CLI
    success, stdout, stderr = run_command("dart pub global activate flutterfire_cli",
                                         description="Instalando FlutterFire CLI",
                                         timeout=120)
    
    if success:
        print_colored("✅ FlutterFire CLI instalado exitosamente", 'green')
        
        # Verificar que está en PATH
        if shutil.which('flutterfire'):
            print_colored("✅ FlutterFire CLI disponible en PATH", 'green')
        else:
            print_colored("⚠️ FlutterFire CLI instalado pero no en PATH", 'yellow')
            print_colored("💡 Agregar ~/.pub-cache/bin al PATH", 'yellow')
        
        return True
    else:
        print_colored("❌ Falló la instalación de FlutterFire CLI", 'red')
        return False

def setup_flutter_dependencies():
    """Configura dependencias de Flutter"""
    print_colored("📦 Configurando dependencias Flutter...", 'cyan')
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print_colored("❌ Directorio frontend no encontrado", 'red')
        return False
    
    # Verificar pubspec.yaml
    pubspec_path = frontend_path / "pubspec.yaml"
    if not pubspec_path.exists():
        print_colored("❌ pubspec.yaml no encontrado", 'red')
        return False
    
    # Ejecutar flutter pub get
    success, stdout, stderr = run_command("flutter pub get", 
                                         cwd=frontend_path,
                                         description="Obteniendo dependencias Flutter",
                                         timeout=180)
    
    if not success:
        print_colored("❌ Falló flutter pub get", 'red')
        return False
    
    print_colored("✅ Dependencias Flutter configuradas", 'green')
    return True

def setup_firebase_functions_dependencies():
    """Configura dependencias de Firebase Functions"""
    print_colored("⚙️ Configurando dependencias Firebase Functions...", 'cyan')
    
    functions_path = Path("backend/functions")
    if not functions_path.exists():
        print_colored("❌ Directorio backend/functions no encontrado", 'red')
        return False
    
    # Verificar package.json
    package_json_path = functions_path / "package.json"
    if not package_json_path.exists():
        print_colored("❌ package.json no encontrado en functions", 'red')
        return False
    
    # Ejecutar npm install
    success, stdout, stderr = run_command("npm install", 
                                         cwd=functions_path,
                                         description="Instalando dependencias Functions",
                                         timeout=300)
    
    if not success:
        print_colored("❌ Falló npm install en functions", 'red')
        return False
    
    print_colored("✅ Dependencias Functions configuradas", 'green')
    return True

def create_environment_files():
    """Crea archivos de entorno necesarios"""
    print_colored("📝 Creando archivos de entorno...", 'cyan')
    
    # Crear .env para backend si no existe
    backend_env_path = Path("backend/.env")
    if not backend_env_path.exists():
        env_content = """# Firebase Project Configuration
FIREBASE_PROJECT_ID=your-project-name
FIREBASE_REGION=us-central1
FIREBASE_STORAGE_BUCKET=your-project.appspot.com

# Development Settings
NODE_ENV=development
FUNCTIONS_EMULATOR_HOST=localhost
FUNCTIONS_EMULATOR_PORT=5001
FIRESTORE_EMULATOR_HOST=localhost:8080
"""
        try:
            with open(backend_env_path, 'w') as f:
                f.write(env_content)
            print_colored("✅ Archivo .env creado en backend/", 'green')
        except Exception as e:
            print_colored(f"❌ Error creando .env: {e}", 'red')
    
    # Crear .gitignore principal si no existe
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        gitignore_content = """# Dependencies
node_modules/
.pub-cache/

# Build outputs
frontend/build/
backend/functions/lib/

# Environment files
.env
.env.local

# Firebase
.firebase/
firebase-debug.log
firestore-debug.log
ui-debug.log

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
"""
        try:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print_colored("✅ Archivo .gitignore creado", 'green')
        except Exception as e:
            print_colored(f"❌ Error creando .gitignore: {e}", 'red')

def run_final_validation():
    """Ejecuta validación final del setup"""
    print_colored("🔍 Ejecutando validación final...", 'cyan')
    
    # Verificar si existe el script de validación mejorado
    if Path("scripts/validate_setup_improved.py").exists():
        success, stdout, stderr = run_command("python scripts/validate_setup_improved.py",
                                             description="Validación completa",
                                             timeout=120)
        return success
    elif Path("scripts/validate_setup.py").exists():
        success, stdout, stderr = run_command("python scripts/validate_setup.py",
                                             description="Validación básica",
                                             timeout=120)
        return success
    else:
        print_colored("⚠️ Script de validación no encontrado", 'yellow')
        return True

def show_setup_summary():
    """Muestra resumen del setup"""
    print_colored("\n" + "="*60, 'cyan')
    print_colored("🎉 SETUP COMPLETADO", 'green')
    print_colored("="*60, 'cyan')
    
    print_colored("\n📋 Próximos pasos:", 'white')
    print_colored("1. Configurar proyecto Firebase:", 'white')
    print_colored("   cd backend && firebase init", 'cyan')
    print_colored("\n2. Configurar FlutterFire:", 'white')
    print_colored("   cd frontend && flutterfire configure", 'cyan')
    print_colored("\n3. Iniciar desarrollo:", 'white')
    print_colored("   python scripts/dev.py", 'cyan')
    print_colored("\n4. Abrir en navegador:", 'white')
    print_colored("   http://localhost:3000", 'cyan')
    
    print_colored("\n📚 Documentación:", 'white')
    print_colored("   📖 Setup completo: docs/HISTORIA_1_1_SETUP.md", 'white')
    print_colored("   🐛 Troubleshooting: docs/HISTORIA_1_1_SETUP.md#troubleshooting", 'white')

def main():
    """Función principal de setup"""
    print_colored("🚀 Setup Automático - Historia 1.1: Registro de Usuario", 'green')
    print_colored("🔧 Configurando entorno de desarrollo...\n", 'cyan')
    
    # Detectar sistema
    system_info = detect_system_info()
    
    # Lista de pasos del setup
    setup_steps = [
        ("Dependencias del sistema", setup_system_dependencies),
        ("Flutter", setup_flutter),
        ("Firebase CLI", setup_firebase_cli),
        ("FlutterFire CLI", setup_flutterfire_cli),
        ("Dependencias Flutter", setup_flutter_dependencies),
        ("Dependencias Functions", setup_firebase_functions_dependencies),
        ("Archivos de entorno", create_environment_files),
        ("Validación final", run_final_validation)
    ]
    
    failed_steps = []
    
    for step_name, step_function in setup_steps:
        print_colored(f"\n{'='*50}", 'blue')
        print_colored(f"🔄 PASO: {step_name}", 'blue')
        print_colored(f"{'='*50}", 'blue')
        
        try:
            success = step_function()
            if success:
                print_colored(f"✅ {step_name} - COMPLETADO", 'green')
            else:
                print_colored(f"❌ {step_name} - FALLÓ", 'red')
                failed_steps.append(step_name)
        except Exception as e:
            print_colored(f"❌ {step_name} - ERROR: {e}", 'red')
            failed_steps.append(step_name)
    
    # Mostrar resumen final
    print_colored(f"\n{'='*60}", 'white')
    
    if not failed_steps:
        print_colored("🎉 ¡SETUP COMPLETADO EXITOSAMENTE!", 'green')
        show_setup_summary()
        return 0
    else:
        print_colored("⚠️ Setup completado con errores", 'yellow')
        print_colored(f"❌ Pasos fallidos: {', '.join(failed_steps)}", 'red')
        print_colored("\n💡 Revisa los errores y ejecuta setup nuevamente", 'yellow')
        print_colored("📖 Consulta: docs/HISTORIA_1_1_SETUP.md", 'cyan')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
