#!/usr/bin/env python3
"""
Setup Script para Historia 1.1: Registro de Usuario
Versión mejorada con validaciones automáticas
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_colored(message, color='white'):
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['white'])}{message}{colors['reset']}")

def run_command(command, cwd=None, description=""):
    """Ejecuta un comando y retorna True si fue exitoso"""
    if description:
        print_colored(f"🔄 {description}...", 'yellow')
    
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        
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
            
    except Exception as e:
        if description:
            print_colored(f"❌ Error ejecutando {description}: {e}", 'red')
        return False, "", str(e)

def check_dependency(command, name, install_command=None):
    """Verifica si una dependencia está instalada"""
    if shutil.which(command.split()[0]):
        success, stdout, stderr = run_command(f"{command} --version")
        if success:
            version = stdout.split('\n')[0] if stdout else "Unknown"
            print_colored(f"✅ {name} encontrado: {version}", 'green')
            return True
        else:
            print_colored(f"⚠️ {name} encontrado pero no responde correctamente", 'yellow')
    
    print_colored(f"❌ {name} no encontrado", 'red')
    
    if install_command:
        print_colored(f"   Ejecutando: {install_command}", 'yellow')
        success, stdout, stderr = run_command(install_command, description=f"Instalando {name}")
        return success
    else:
        print_colored(f"   Instala {name} manualmente", 'white')
        return False

def validate_and_fix_flutter():
    """Valida y configura Flutter correctamente"""
    print_colored("� Configurando Flutter...", 'cyan')
    
    # Verificar Flutter
    if not check_dependency("flutter", "Flutter"):
        print_colored("   Instala Flutter desde: https://flutter.dev/docs/get-started/install", 'white')
        return False
    
    # Habilitar web
    success, stdout, stderr = run_command("flutter config --enable-web", description="Habilitando Flutter Web")
    if not success:
        print_colored("⚠️ No se pudo habilitar Flutter Web automáticamente", 'yellow')
    
    # Verificar web habilitado
    success, stdout, stderr = run_command("flutter config")
    if success and "enable-web: true" in stdout:
        print_colored("✅ Flutter Web habilitado", 'green')
    else:
        print_colored("❌ Flutter Web no está habilitado", 'red')
        return False
    
    return True

def setup_flutter_dependencies():
    """Configura dependencias de Flutter"""
    print_colored("📱 Configurando dependencias Flutter...", 'cyan')
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print_colored("❌ Directorio frontend no encontrado", 'red')
        return False
    
    # Limpiar primero
    run_command("flutter clean", cwd=frontend_path, description="Limpiando cache Flutter")
    
    # Instalar dependencias
    success, stdout, stderr = run_command("flutter pub get", cwd=frontend_path, description="Instalando dependencias Flutter")
    if not success:
        print_colored("❌ Error instalando dependencias Flutter", 'red')
        return False
    
    # Verificar dependencias críticas
    pubspec_path = frontend_path / "pubspec.yaml"
    if pubspec_path.exists():
        with open(pubspec_path, 'r') as f:
            content = f.read()
            required_deps = ['firebase_core', 'firebase_auth', 'cloud_firestore', 'flutter_bloc']
            missing_deps = []
            
            for dep in required_deps:
                if dep not in content:
                    missing_deps.append(dep)
            
            if missing_deps:
                print_colored(f"⚠️ Dependencias faltantes en pubspec.yaml: {missing_deps}", 'yellow')
                print_colored("   Actualiza pubspec.yaml manualmente", 'white')
            else:
                print_colored("✅ Todas las dependencias Firebase están presentes", 'green')
    
    return True

def setup_firebase_functions():
    """Configura Firebase Functions"""
    print_colored("🔥 Configurando Firebase Functions...", 'cyan')
    
    functions_path = Path("backend/functions")
    if not functions_path.exists():
        print_colored("❌ Directorio backend/functions no encontrado", 'red')
        return False
    
    # Verificar package.json
    package_json_path = functions_path / "package.json"
    if not package_json_path.exists():
        print_colored("❌ package.json no encontrado en functions", 'red')
        return False
    
    # Instalar dependencias
    success, stdout, stderr = run_command("npm install", cwd=functions_path, description="Instalando dependencias Functions")
    if not success:
        print_colored("❌ Error instalando dependencias Functions", 'red')
        return False
    
    # Verificar TypeScript
    success, stdout, stderr = run_command("npm run build", cwd=functions_path, description="Compilando TypeScript Functions")
    if not success:
        print_colored("⚠️ Error compilando TypeScript, pero continuando...", 'yellow')
    
    return True

def check_firebase_cli():
    """Verifica y configura Firebase CLI"""
    print_colored("🔧 Verificando Firebase CLI...", 'cyan')
    
    # Intentar instalar Firebase CLI si no existe
    if not check_dependency("firebase", "Firebase CLI", "npm install -g firebase-tools"):
        print_colored("❌ No se pudo instalar Firebase CLI automáticamente", 'red')
        print_colored("   Ejecuta manualmente: npm install -g firebase-tools", 'white')
        return False
    
    # Verificar login (no obligatorio para setup)
    success, stdout, stderr = run_command("firebase projects:list")
    if "Error: Not logged in" in stderr:
        print_colored("⚠️ No estás logueado en Firebase", 'yellow')
        print_colored("   Ejecuta: firebase login", 'white')
    elif success:
        print_colored("✅ Firebase CLI configurado y logueado", 'green')
    
    return True

def validate_project_structure():
    """Valida estructura básica del proyecto"""
    print_colored("📁 Validando estructura del proyecto...", 'cyan')
    
    critical_files = [
        "frontend/pubspec.yaml",
        "frontend/lib/main.dart",
        "backend/firebase.json",
        "backend/firestore.rules"
    ]
    
    missing_files = []
    for file_path in critical_files:
        if Path(file_path).exists():
            print_colored(f"✅ {file_path}", 'green')
        else:
            missing_files.append(file_path)
            print_colored(f"❌ {file_path} - FALTANTE", 'red')
    
    if missing_files:
        print_colored("❌ Algunos archivos críticos faltan", 'red')
        return False
    
    print_colored("✅ Estructura básica correcta", 'green')
    return True

def show_next_steps():
    """Muestra próximos pasos después del setup"""
    print_colored("\n📋 Próximos pasos:", 'cyan')
    print_colored("1. Configurar Firebase project:", 'white')
    print_colored("   cd backend && firebase init", 'white')
    print_colored("", 'white')
    print_colored("2. Configurar Flutter con Firebase:", 'white')
    print_colored("   cd frontend && flutterfire configure --project=tu-proyecto", 'white')
    print_colored("", 'white')
    print_colored("3. Validar setup completo:", 'white')
    print_colored("   python scripts/validate_setup.py", 'white')
    print_colored("", 'white')
    print_colored("4. Iniciar desarrollo:", 'white')
    print_colored("   python scripts/dev.py", 'white')
    print_colored("", 'white')
    print_colored("📖 Guía detallada: docs/HISTORIA_1_1_SETUP.md", 'yellow')

def main():
    print_colored("🚀 Setup Historia 1.1: Registro de Usuario", 'green')
    print_colored("   Versión mejorada con validaciones automáticas\n", 'white')
    
    # Verificar dependencias principales
    print_colored("📋 Verificando dependencias...", 'yellow')
    
    dependencies_ok = True
    
    # Node.js
    if not check_dependency("node", "Node.js"):
        print_colored("   Instala Node.js desde: https://nodejs.org/", 'white')
        dependencies_ok = False
    
    # Flutter
    if not validate_and_fix_flutter():
        dependencies_ok = False
    
    # Firebase CLI
    if not check_firebase_cli():
        dependencies_ok = False
    
    if not dependencies_ok:
        print_colored("\n❌ Faltan dependencias críticas.", 'red')
        print_colored("   Instala las dependencias faltantes y ejecuta el script nuevamente.", 'white')
        return 1
    
    print_colored("\n✅ Dependencias verificadas\n", 'green')
    
    # Setup de componentes
    setup_steps = [
        ("Estructura del proyecto", validate_project_structure),
        ("Dependencias Flutter", setup_flutter_dependencies),
        ("Firebase Functions", setup_firebase_functions)
    ]
    
    failed_steps = []
    for description, step_function in setup_steps:
        if not step_function():
            failed_steps.append(description)
    
    print_colored("\n" + "="*60, 'white')
    
    if not failed_steps:
        print_colored("🎉 Setup básico completado exitosamente!", 'green')
        show_next_steps()
        return 0
    else:
        print_colored(f"⚠️ Setup completado con {len(failed_steps)} advertencia(s):", 'yellow')
        for step in failed_steps:
            print_colored(f"   - {step}", 'yellow')
        show_next_steps()
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
