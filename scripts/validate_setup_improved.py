#!/usr/bin/env python3
"""
Script avanzado para validar que el setup de Historia 1.1 está completo
Ejecutar: python scripts/validate_setup_improved.py

Versión mejorada con:
- Validación más exhaustiva
- Diagnósticos automáticos  
- Sugerencias de solución
- Métricas de salud del proyecto
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Tuple, List, Dict, Optional

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

def run_command(command, cwd=None, timeout=30):
    """Ejecuta un comando y retorna True si fue exitoso"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout}s"
    except Exception as e:
        return False, "", str(e)

class ValidationResults:
    def __init__(self):
        self.results = []
        self.warnings = []
        self.errors = []
        
    def add_result(self, category: str, item: str, status: bool, message: str = "", suggestion: str = ""):
        """Añade resultado de validación"""
        result = {
            'category': category,
            'item': item,
            'status': status,
            'message': message,
            'suggestion': suggestion
        }
        self.results.append(result)
        
        if not status:
            self.errors.append(f"{category}: {item} - {message}")
            if suggestion:
                self.warnings.append(f"💡 {suggestion}")

    def get_summary(self):
        """Retorna resumen de validación"""
        total = len(self.results)
        passed = len([r for r in self.results if r['status']])
        failed = total - passed
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / total * 100) if total > 0 else 0
        }

def validate_project_structure(results: ValidationResults):
    """Valida que la estructura del proyecto esté completa"""
    print_colored("🔍 Validando estructura del proyecto...", 'cyan')
    
    # Archivos críticos del frontend
    frontend_files = [
        "frontend/lib/models/user.dart",
        "frontend/lib/services/auth_service.dart", 
        "frontend/lib/services/auth_bloc.dart",
        "frontend/lib/screens/auth/register_screen.dart",
        "frontend/lib/screens/auth/login_screen.dart",
        "frontend/lib/widgets/custom_text_field.dart",
        "frontend/lib/widgets/custom_button.dart",
        "frontend/lib/main.dart",
        "frontend/pubspec.yaml",
        "frontend/web/index.html"
    ]
    
    # Archivos críticos del backend
    backend_files = [
        "backend/functions/src/index.ts",
        "backend/functions/package.json",
        "backend/functions/tsconfig.json",
        "backend/firebase.json",
        "backend/firestore.rules",
        "backend/.firebaserc"
    ]
    
    # Archivos de scripts y documentación
    tooling_files = [
        "scripts/setup.py",
        "scripts/validate_setup.py",
        "scripts/dev.py",
        "scripts/test.py",
        "scripts/deploy.py",
        "docs/HISTORIA_1_1_SETUP.md",
        "README.md",
        ".gitignore"
    ]
    
    all_files = frontend_files + backend_files + tooling_files
    
    for file_path in all_files:
        path = Path(file_path)
        if path.exists():
            # Verificar si el archivo no está vacío
            if path.stat().st_size > 0:
                print_colored(f"  ✅ {file_path}", 'green')
                results.add_result("Structure", file_path, True)
            else:
                print_colored(f"  ⚠️ {file_path} (archivo vacío)", 'yellow')
                results.add_result("Structure", file_path, False, "Archivo vacío", 
                                 f"Revisar contenido de {file_path}")
        else:
            print_colored(f"  ❌ {file_path}", 'red')
            results.add_result("Structure", file_path, False, "Archivo faltante",
                             f"Crear archivo {file_path}")
    
    # Verificar directorios importantes
    important_dirs = [
        "frontend/lib",
        "frontend/web", 
        "backend/functions/src",
        "scripts",
        "docs"
    ]
    
    for dir_path in important_dirs:
        if Path(dir_path).exists():
            print_colored(f"  ✅ {dir_path}/", 'green')
            results.add_result("Structure", f"{dir_path}/", True)
        else:
            print_colored(f"  ❌ {dir_path}/", 'red')
            results.add_result("Structure", f"{dir_path}/", False, "Directorio faltante",
                             f"Crear directorio {dir_path}")

def validate_flutter_setup(results: ValidationResults):
    """Valida que Flutter esté correctamente configurado"""
    print_colored("🔍 Validando configuración Flutter...", 'cyan')
    
    # Verificar Flutter instalado
    success, stdout, stderr = run_command("flutter --version")
    if not success:
        print_colored("❌ Flutter no está instalado o no está en PATH", 'red')
        results.add_result("Flutter", "Installation", False, "Flutter no encontrado",
                         "Instalar Flutter desde https://flutter.dev/docs/get-started/install")
        return
    
    # Extraer versión de Flutter
    flutter_version = "Unknown"
    if stdout:
        lines = stdout.split('\n')
        for line in lines:
            if 'Flutter' in line and ('•' in line or 'channel' in line):
                flutter_version = line.strip()
                break
    
    print_colored(f"  ✅ Flutter instalado: {flutter_version}", 'green')
    results.add_result("Flutter", "Installation", True, flutter_version)
    
    # Verificar web habilitado
    success, stdout, stderr = run_command("flutter config")
    if success and "enable-web: true" in stdout:
        print_colored("  ✅ Flutter Web habilitado", 'green')
        results.add_result("Flutter", "Web Support", True)
    else:
        print_colored("❌ Flutter Web no está habilitado", 'red')
        results.add_result("Flutter", "Web Support", False, "Web no habilitado",
                         "Ejecutar: flutter config --enable-web")
    
    # Verificar devices disponibles
    success, stdout, stderr = run_command("flutter devices")
    if success and ("Chrome" in stdout or "chrome" in stdout):
        print_colored("  ✅ Chrome disponible para desarrollo", 'green')
        results.add_result("Flutter", "Chrome Device", True)
    else:
        print_colored("  ⚠️ Chrome no detectado como device", 'yellow')
        results.add_result("Flutter", "Chrome Device", False, "Chrome no disponible",
                         "Verificar instalación de Chrome")
    
    # Verificar pubspec.yaml
    pubspec_path = Path("frontend/pubspec.yaml")
    if pubspec_path.exists():
        try:
            with open(pubspec_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            required_deps = [
                'firebase_core',
                'firebase_auth', 
                'cloud_firestore',
                'flutter_bloc',
                'equatable'
            ]
            
            missing_deps = []
            for dep in required_deps:
                if dep not in content:
                    missing_deps.append(dep)
            
            if missing_deps:
                print_colored(f"  ❌ Dependencias faltantes: {missing_deps}", 'red')
                results.add_result("Flutter", "Dependencies", False, 
                                 f"Faltan: {', '.join(missing_deps)}",
                                 "Ejecutar: flutter pub add <dependencia>")
            else:
                print_colored("  ✅ Dependencias Firebase correctas", 'green')
                results.add_result("Flutter", "Dependencies", True)
                
        except Exception as e:
            print_colored(f"  ❌ Error leyendo pubspec.yaml: {e}", 'red')
            results.add_result("Flutter", "Dependencies", False, str(e))
    
    # Verificar firebase_options.dart
    firebase_options_path = Path("frontend/lib/firebase_options.dart")
    if firebase_options_path.exists():
        try:
            with open(firebase_options_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if "DefaultFirebaseOptions" in content and "web" in content:
                print_colored("  ✅ firebase_options.dart configurado correctamente", 'green')
                results.add_result("Flutter", "Firebase Options", True)
            else:
                print_colored("  ⚠️ firebase_options.dart incompleto", 'yellow')
                results.add_result("Flutter", "Firebase Options", False, 
                                 "Configuración incompleta",
                                 "Ejecutar: flutterfire configure --project=tu-proyecto")
        except Exception as e:
            print_colored(f"  ❌ Error leyendo firebase_options.dart: {e}", 'red')
            results.add_result("Flutter", "Firebase Options", False, str(e))
    else:
        print_colored("  ❌ firebase_options.dart no encontrado", 'red')
        results.add_result("Flutter", "Firebase Options", False, "Archivo no encontrado",
                         "Ejecutar: flutterfire configure --project=tu-proyecto")

def validate_firebase_setup(results: ValidationResults):
    """Valida que Firebase esté correctamente configurado"""
    print_colored("🔍 Validando configuración Firebase...", 'cyan')
    
    # Verificar Firebase CLI
    success, stdout, stderr = run_command("firebase --version")
    if not success:
        print_colored("❌ Firebase CLI no está instalado", 'red')
        results.add_result("Firebase", "CLI", False, "Firebase CLI no encontrado",
                         "Ejecutar: npm install -g firebase-tools")
        return
    
    print_colored(f"  ✅ Firebase CLI instalado: {stdout.strip()}", 'green')
    results.add_result("Firebase", "CLI", True, stdout.strip())
    
    # Verificar .firebaserc
    firebaserc_path = Path("backend/.firebaserc")
    if firebaserc_path.exists():
        try:
            with open(firebaserc_path, 'r') as f:
                config = json.load(f)
            if 'projects' in config and 'default' in config['projects']:
                project_id = config['projects']['default']
                print_colored(f"  ✅ Proyecto configurado: {project_id}", 'green')
                results.add_result("Firebase", "Project Config", True, project_id)
            else:
                print_colored("❌ .firebaserc mal configurado", 'red')
                results.add_result("Firebase", "Project Config", False, ".firebaserc mal configurado")
        except json.JSONDecodeError:
            print_colored("❌ .firebaserc no es un JSON válido", 'red')
            results.add_result("Firebase", "Project Config", False, "JSON inválido")
    else:
        print_colored("❌ .firebaserc no encontrado", 'red')
        results.add_result("Firebase", "Project Config", False, "Archivo no encontrado",
                         "Ejecutar: firebase init en directorio backend/")
    
    # Verificar firebase.json
    firebase_json_path = Path("backend/firebase.json")
    if firebase_json_path.exists():
        try:
            with open(firebase_json_path, 'r') as f:
                config = json.load(f)
            required_features = ['hosting', 'functions', 'firestore']
            missing_features = []
            
            for feature in required_features:
                if feature not in config:
                    missing_features.append(feature)
            
            if missing_features:
                print_colored(f"❌ Features faltantes en firebase.json: {missing_features}", 'red')
                results.add_result("Firebase", "Config Features", False, 
                                 f"Faltan: {', '.join(missing_features)}")
            else:
                print_colored("  ✅ firebase.json configurado correctamente", 'green')
                results.add_result("Firebase", "Config Features", True)
        except json.JSONDecodeError:
            print_colored("❌ firebase.json no es un JSON válido", 'red')
            results.add_result("Firebase", "Config Features", False, "JSON inválido")
    else:
        print_colored("❌ firebase.json no encontrado", 'red')
        results.add_result("Firebase", "Config Features", False, "Archivo no encontrado")
    
    # Verificar Node.js y npm
    success, stdout, stderr = run_command("node --version")
    if not success:
        print_colored("❌ Node.js no está instalado", 'red')
        results.add_result("Firebase", "Node.js", False, "Node.js no encontrado")
        return
    
    print_colored(f"  ✅ Node.js instalado: {stdout.strip()}", 'green')
    results.add_result("Firebase", "Node.js", True, stdout.strip())
    
    # Verificar dependencias de Functions
    functions_package_path = Path("backend/functions/package.json")
    if functions_package_path.exists():
        print_colored("  ✅ Functions package.json existe", 'green')
        results.add_result("Firebase", "Functions Package", True)
        
        # Verificar node_modules
        node_modules_path = Path("backend/functions/node_modules")
        if not node_modules_path.exists():
            print_colored("⚠️ node_modules no encontrado en functions", 'yellow')
            results.add_result("Firebase", "Functions Dependencies", False, 
                             "node_modules faltante",
                             "Ejecutar: cd backend/functions && npm install")
        else:
            print_colored("  ✅ Dependencies instaladas en functions", 'green')
            results.add_result("Firebase", "Functions Dependencies", True)
    else:
        print_colored("❌ Functions package.json no encontrado", 'red')
        results.add_result("Firebase", "Functions Package", False, "package.json faltante")

def validate_scripts(results: ValidationResults):
    """Valida que los scripts estén disponibles"""
    print_colored("🔍 Validando scripts de desarrollo...", 'cyan')
    
    required_scripts = [
        "scripts/setup.py",
        "scripts/dev.py", 
        "scripts/test.py",
        "scripts/deploy.py"
    ]
    
    for script_path in required_scripts:
        if Path(script_path).exists():
            print_colored(f"  ✅ {script_path}", 'green')
            results.add_result("Scripts", script_path, True)
        else:
            print_colored(f"  ❌ {script_path}", 'red')
            results.add_result("Scripts", script_path, False, "Script faltante")
    
    # Verificar helpers
    helpers = ["run.bat", "run.sh"]
    for helper in helpers:
        if Path(helper).exists():
            print_colored(f"  ✅ {helper}", 'green')
            results.add_result("Scripts", helper, True)
        else:
            print_colored(f"  ⚠️ {helper} no encontrado", 'yellow')
            results.add_result("Scripts", helper, False, "Helper faltante")

def run_health_checks(results: ValidationResults):
    """Ejecuta verificaciones de salud del sistema"""
    print_colored("🔍 Ejecutando verificaciones de salud...", 'cyan')
    
    # Verificar conectividad a internet
    print_colored("  🌐 Verificando conectividad...", 'blue')
    success, _, _ = run_command("ping -c 1 8.8.8.8", timeout=10)
    if success:
        print_colored("  ✅ Conectividad a internet OK", 'green')
        results.add_result("Health", "Internet", True)
    else:
        print_colored("  ⚠️ Problemas de conectividad", 'yellow')
        results.add_result("Health", "Internet", False, "Sin conectividad")
    
    # Verificar espacio en disco
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (1024**3)
        if free_gb > 2:
            print_colored(f"  ✅ Espacio libre: {free_gb}GB", 'green')
            results.add_result("Health", "Disk Space", True, f"{free_gb}GB libre")
        else:
            print_colored(f"  ⚠️ Poco espacio libre: {free_gb}GB", 'yellow')
            results.add_result("Health", "Disk Space", False, f"Solo {free_gb}GB libre")
    except Exception:
        print_colored("  ⚠️ No se pudo verificar espacio en disco", 'yellow')
        results.add_result("Health", "Disk Space", False, "Error verificando espacio")

def show_detailed_report(results: ValidationResults):
    """Muestra reporte detallado de la validación"""
    summary = results.get_summary()
    
    print_colored("\n" + "="*60, 'white')
    print_colored("📊 REPORTE DETALLADO DE VALIDACIÓN", 'cyan')
    print_colored("="*60, 'white')
    
    # Resumen general
    print_colored(f"\n🎯 Resumen General:", 'white')
    print_colored(f"   Total de verificaciones: {summary['total']}", 'white')
    print_colored(f"   ✅ Exitosas: {summary['passed']}", 'green')
    print_colored(f"   ❌ Fallidas: {summary['failed']}", 'red')
    print_colored(f"   📈 Tasa de éxito: {summary['success_rate']:.1f}%", 'cyan')
    
    # Agrupar por categoría
    categories = {}
    for result in results.results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(result)
    
    # Mostrar por categoría
    for category, items in categories.items():
        passed = len([i for i in items if i['status']])
        total = len(items)
        status_icon = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
        
        print_colored(f"\n{status_icon} {category}: {passed}/{total}", 'cyan')
        
        for item in items:
            status_icon = "✅" if item['status'] else "❌"
            print_colored(f"   {status_icon} {item['item']}", 
                         'green' if item['status'] else 'red')
            if not item['status'] and item['message']:
                print_colored(f"      └── {item['message']}", 'yellow')
    
    # Mostrar sugerencias
    if results.warnings:
        print_colored(f"\n💡 Sugerencias de mejora:", 'yellow')
        for warning in results.warnings[:5]:  # Mostrar solo las primeras 5
            print_colored(f"   {warning}", 'yellow')

def show_next_steps(results: ValidationResults):
    """Muestra los próximos pasos según el estado de validación"""
    summary = results.get_summary()
    
    print_colored("\n📋 Próximos pasos:", 'cyan')
    
    if summary['success_rate'] >= 90:
        print_colored("🎉 ¡Excelente! Tu setup está casi perfecto.", 'green')
        print_colored("1. Iniciar desarrollo: python scripts/dev.py", 'white')
        print_colored("2. Abrir http://localhost:3000 en el navegador", 'white') 
        print_colored("3. Probar registro de usuario", 'white')
        print_colored("4. Verificar usuario en Firebase Console", 'white')
        print_colored("5. Continuar con Historia 1.2: Login de Usuario", 'white')
    elif summary['success_rate'] >= 70:
        print_colored("⚠️ Hay algunos problemas menores que debes resolver.", 'yellow')
        print_colored("1. Revisar los errores mostrados arriba", 'white')
        print_colored("2. Ejecutar: python scripts/setup.py", 'white')
        print_colored("3. Ejecutar nuevamente: python scripts/validate_setup.py", 'white')
    else:
        print_colored("❌ Hay problemas serios que requieren atención.", 'red')
        print_colored("1. Revisar documentación: docs/HISTORIA_1_1_SETUP.md", 'white')
        print_colored("2. Ejecutar setup completo: python scripts/setup.py", 'white')
        print_colored("3. Verificar requisitos del sistema", 'white')
        print_colored("4. Contactar al equipo si persisten los problemas", 'white')

def main():
    """Función principal de validación mejorada"""
    print_colored("🚀 Validación Avanzada - Historia 1.1: Registro de Usuario\n", 'green')
    print_colored("🔍 Ejecutando verificaciones exhaustivas...\n", 'cyan')
    
    results = ValidationResults()
    
    # Ejecutar todas las validaciones
    validate_project_structure(results)
    print()
    validate_flutter_setup(results)
    print()
    validate_firebase_setup(results)
    print()
    validate_scripts(results)
    print()
    run_health_checks(results)
    
    # Mostrar reporte detallado
    show_detailed_report(results)
    
    # Mostrar próximos pasos
    show_next_steps(results)
    
    # Retornar código de salida apropiado
    summary = results.get_summary()
    if summary['success_rate'] >= 90:
        print_colored("\n🎉 ¡Validación completada exitosamente!", 'green')
        return 0
    elif summary['success_rate'] >= 70:
        print_colored("\n⚠️ Validación completada con warnings.", 'yellow')
        return 1
    else:
        print_colored("\n❌ Validación falló. Revisar errores.", 'red')
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
