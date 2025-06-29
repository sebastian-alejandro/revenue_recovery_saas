#!/usr/bin/env python3
"""
Script avanzado para validar que el setup de Historia 1.1 está completo
Ejecutar: python scripts/validate_setup.py

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
import requests
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

def check_url_accessible(url, timeout=5):
    """Verifica si una URL es accesible"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except Exception:
        return False

class EnvironmentValidator:
    def __init__(self):
        self.validation_results = []
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
        self.validation_results.append(result)
        
        if not status:
            self.errors.append(f"{category}: {item} - {message}")
            if suggestion:
                self.warnings.append(f"💡 {suggestion}")

    def validate_project_structure(self):
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
        missing_files = []
        
        for file_path in all_files:
            path = Path(file_path)
            if path.exists():
                # Verificar si el archivo no está vacío
                if path.stat().st_size > 0:
                    print_colored(f"  ✅ {file_path}", 'green')
                    self.add_result("Structure", file_path, True)
                else:
                    print_colored(f"  ⚠️ {file_path} (archivo vacío)", 'yellow')
                    self.add_result("Structure", file_path, False, "Archivo vacío", 
                                   f"Revisar contenido de {file_path}")
            else:
                missing_files.append(file_path)
                print_colored(f"  ❌ {file_path}", 'red')
                self.add_result("Structure", file_path, False, "Archivo faltante",
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
            else:
                print_colored(f"  ❌ {dir_path}/", 'red')
                self.add_result("Structure", f"{dir_path}/", False, "Directorio faltante",
                               f"Crear directorio {dir_path}")
        
        success = len(missing_files) == 0
        if success:
            print_colored("✅ Estructura del proyecto completa", 'green')
        else:
            print_colored(f"❌ {len(missing_files)} archivos faltantes", 'red')
            
        return success

    def validate_flutter_setup(self):
        """Valida que Flutter esté correctamente configurado"""
        print_colored("🔍 Validando configuración Flutter...", 'cyan')
        
        # Verificar Flutter instalado
        success, stdout, stderr = run_command("flutter --version")
        if not success:
            print_colored("❌ Flutter no está instalado o no está en PATH", 'red')
            self.add_result("Flutter", "Installation", False, "Flutter no encontrado",
                           "Instalar Flutter desde https://flutter.dev/docs/get-started/install")
            return False
        
        # Extraer versión de Flutter
        flutter_version = "Unknown"
        if stdout:
            lines = stdout.split('\n')
            for line in lines:
                if 'Flutter' in line and '•' in line:
                    flutter_version = line.split('•')[0].strip()
                    break
        
        print_colored(f"  ✅ Flutter instalado: {flutter_version}", 'green')
        self.add_result("Flutter", "Installation", True, flutter_version)
        
        # Verificar web habilitado
        success, stdout, stderr = run_command("flutter config")
        web_enabled = False
        if success and "enable-web: true" in stdout:
            web_enabled = True
            print_colored("  ✅ Flutter Web habilitado", 'green')
            self.add_result("Flutter", "Web Support", True)
        else:
            print_colored("❌ Flutter Web no está habilitado", 'red')
            self.add_result("Flutter", "Web Support", False, "Web no habilitado",
                           "Ejecutar: flutter config --enable-web")
        
        # Verificar devices disponibles
        success, stdout, stderr = run_command("flutter devices")
        chrome_available = False
        if success and ("Chrome" in stdout or "chrome" in stdout):
            chrome_available = True
            print_colored("  ✅ Chrome disponible para desarrollo", 'green')
            self.add_result("Flutter", "Chrome Device", True)
        else:
            print_colored("  ⚠️ Chrome no detectado como device", 'yellow')
            self.add_result("Flutter", "Chrome Device", False, "Chrome no disponible",
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
                    self.add_result("Flutter", "Dependencies", False, 
                                   f"Faltan: {', '.join(missing_deps)}",
                                   "Ejecutar: flutter pub add <dependencia>")
                else:
                    print_colored("  ✅ Dependencias Firebase correctas", 'green')
                    self.add_result("Flutter", "Dependencies", True)
                    
            except Exception as e:
                print_colored(f"  ❌ Error leyendo pubspec.yaml: {e}", 'red')
                self.add_result("Flutter", "Dependencies", False, str(e))
        
        # Verificar firebase_options.dart
        firebase_options_path = Path("frontend/lib/firebase_options.dart")
        if firebase_options_path.exists():
            try:
                with open(firebase_options_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "DefaultFirebaseOptions" in content and "web" in content:
                        print_colored("  ✅ firebase_options.dart configurado correctamente", 'green')
                        self.add_result("Flutter", "Firebase Options", True)
                    else:
                        print_colored("  ⚠️ firebase_options.dart incompleto", 'yellow')
                        self.add_result("Flutter", "Firebase Options", False, 
                                       "Configuración incompleta",
                                       "Ejecutar: flutterfire configure --project=tu-proyecto")
            except Exception as e:
                print_colored(f"  ❌ Error leyendo firebase_options.dart: {e}", 'red')
                self.add_result("Flutter", "Firebase Options", False, str(e))
        else:
            print_colored("  ❌ firebase_options.dart no encontrado", 'red')
            self.add_result("Flutter", "Firebase Options", False, "Archivo no encontrado",
                           "Ejecutar: flutterfire configure --project=tu-proyecto")
        
        # Verificar flutter doctor
        print_colored("  🔍 Ejecutando flutter doctor...", 'blue')
        success, stdout, stderr = run_command("flutter doctor", timeout=45)
        if success:
            # Analizar salida de flutter doctor
            issues = []
            if "✗" in stdout:
                lines = stdout.split('\n')
                for line in lines:
                    if "✗" in line:
                        issues.append(line.strip())
            
            if issues:
                print_colored(f"  ⚠️ Flutter doctor encontró {len(issues)} problemas", 'yellow')
                for issue in issues[:3]:  # Mostrar solo los primeros 3
                    print_colored(f"    - {issue}", 'yellow')
                self.add_result("Flutter", "Doctor", False, f"{len(issues)} problemas encontrados",
                               "Ejecutar: flutter doctor -v para más detalles")
            else:
                print_colored("  ✅ Flutter doctor: todo correcto", 'green')
                self.add_result("Flutter", "Doctor", True)
        
        overall_success = web_enabled and chrome_available
        if overall_success:
            print_colored("✅ Flutter configurado correctamente", 'green')
        else:
            print_colored("❌ Flutter requiere configuración adicional", 'red')
            
        return overall_success
                    missing_deps.append(dep)
            
            if missing_deps:
                print_colored(f"❌ Dependencias faltantes en pubspec.yaml: {missing_deps}", 'red')
                return False
            
            print_colored("  ✅ Dependencias Firebase correctas", 'green')
    
    # Verificar firebase_options.dart
    firebase_options_path = Path("frontend/lib/firebase_options.dart")
    if not firebase_options_path.exists():
        print_colored("❌ firebase_options.dart no encontrado", 'red')
        print_colored("   Ejecutar: flutterfire configure --project=revenue-recovery-saas", 'yellow')
        return False
    
    print_colored("  ✅ firebase_options.dart existe", 'green')
    
    print_colored("✅ Flutter configurado correctamente", 'green')
    return True

def validate_firebase_setup():
    """Valida que Firebase esté correctamente configurado"""
    print_colored("🔍 Validando configuración Firebase...", 'cyan')
    
    # Verificar Firebase CLI
    success, stdout, stderr = run_command("firebase --version")
    if not success:
        print_colored("❌ Firebase CLI no está instalado", 'red')
        print_colored("   Ejecutar: npm install -g firebase-tools", 'yellow')
        return False
    
    print_colored(f"  ✅ Firebase CLI instalado: {stdout.strip()}", 'green')
    
    # Verificar .firebaserc
    firebaserc_path = Path("backend/.firebaserc")
    if firebaserc_path.exists():
        try:
            with open(firebaserc_path, 'r') as f:
                config = json.load(f)
                if 'projects' in config and 'default' in config['projects']:
                    project_id = config['projects']['default']
                    print_colored(f"  ✅ Proyecto configurado: {project_id}", 'green')
                else:
                    print_colored("❌ .firebaserc mal configurado", 'red')
                    return False
        except json.JSONDecodeError:
            print_colored("❌ .firebaserc no es un JSON válido", 'red')
            return False
    else:
        print_colored("❌ .firebaserc no encontrado", 'red')
        print_colored("   Ejecutar: firebase init en directorio backend/", 'yellow')
        return False
    
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
                    return False
                
                print_colored("  ✅ firebase.json configurado correctamente", 'green')
        except json.JSONDecodeError:
            print_colored("❌ firebase.json no es un JSON válido", 'red')
            return False
    else:
        print_colored("❌ firebase.json no encontrado", 'red')
        return False
    
    # Verificar Node.js y npm
    success, stdout, stderr = run_command("node --version")
    if not success:
        print_colored("❌ Node.js no está instalado", 'red')
        return False
    
    print_colored(f"  ✅ Node.js instalado: {stdout.strip()}", 'green')
    
    # Verificar dependencias de Functions
    functions_package_path = Path("backend/functions/package.json")
    if functions_package_path.exists():
        print_colored("  ✅ Functions package.json existe", 'green')
        
        # Verificar node_modules
        node_modules_path = Path("backend/functions/node_modules")
        if not node_modules_path.exists():
            print_colored("⚠️ node_modules no encontrado en functions", 'yellow')
            print_colored("   Ejecutar: cd backend/functions && npm install", 'yellow')
        else:
            print_colored("  ✅ Dependencies instaladas en functions", 'green')
    
    print_colored("✅ Firebase configurado correctamente", 'green')
    return True

def validate_scripts():
    """Valida que los scripts estén disponibles"""
    print_colored("🔍 Validando scripts de desarrollo...", 'cyan')
    
    required_scripts = [
        "scripts/setup.py",
        "scripts/dev.py", 
        "scripts/test.py",
        "scripts/deploy.py"
    ]
    
    missing_scripts = []
    for script_path in required_scripts:
        if not Path(script_path).exists():
            missing_scripts.append(script_path)
        else:
            print_colored(f"  ✅ {script_path}", 'green')
    
    if missing_scripts:
        print_colored(f"❌ Scripts faltantes: {missing_scripts}", 'red')
        return False
    
    # Verificar helpers
    helpers = ["run.bat", "run.sh"]
    for helper in helpers:
        if Path(helper).exists():
            print_colored(f"  ✅ {helper}", 'green')
    
    print_colored("✅ Scripts disponibles", 'green')
    return True

def show_next_steps():
    """Muestra los próximos pasos después de la validación"""
    print_colored("\n📋 Próximos pasos:", 'cyan')
    print_colored("1. Iniciar desarrollo: python scripts/dev.py", 'white')
    print_colored("2. Abrir http://localhost:3000 en el navegador", 'white') 
    print_colored("3. Probar registro de usuario", 'white')
    print_colored("4. Verificar usuario en Firebase Console", 'white')
    print_colored("5. Continuar con Historia 1.2: Login de Usuario", 'white')

def main():
    """Función principal de validación"""
    print_colored("🚀 Validando Setup Historia 1.1: Registro de Usuario\n", 'green')
    
    validations = [
        validate_project_structure(),
        validate_flutter_setup(),
        validate_firebase_setup(),
        validate_scripts()
    ]
    
    print_colored("\n" + "="*60, 'white')
    
    if all(validations):
        print_colored("🎉 ¡Setup completado exitosamente!", 'green')
        print_colored("✅ Todos los componentes están configurados correctamente", 'green')
        show_next_steps()
        return 0
    else:
        print_colored("❌ Setup incompleto. Revisar errores arriba.", 'red')
        print_colored("📖 Consultar: docs/HISTORIA_1_1_SETUP.md", 'yellow')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
