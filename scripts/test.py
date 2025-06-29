#!/usr/bin/env python3
"""
Script de Testing - Historia 1.1
Ejecuta tests de Flutter y validaciones del código
"""

import os
import sys
import subprocess
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
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_colored(f"✅ {description} - Exitoso", 'green')
            if result.stdout.strip():
                print(result.stdout.strip())
            return True
        else:
            print_colored(f"❌ {description} - Falló", 'red')
            if result.stderr.strip():
                print(result.stderr.strip())
            return False
            
    except Exception as e:
        print_colored(f"❌ Error ejecutando {description}: {e}", 'red')
        return False

def main():
    print_colored("🧪 Ejecutando tests Historia 1.1...", 'green')
    print()
    
    # Verificar que estamos en el directorio correcto
    if not Path("frontend").exists():
        print_colored("❌ Directorio frontend no encontrado", 'red')
        sys.exit(1)
    
    total_tests = 0
    passed_tests = 0
    
    # Flutter Analysis
    print_colored("📋 Análisis de código Flutter...", 'cyan')
    if run_command("flutter analyze", cwd="frontend", description="Análisis estático"):
        passed_tests += 1
    total_tests += 1
    
    # Flutter Format Check
    print_colored("🎨 Verificando formato de código...", 'cyan')
    if run_command("flutter format --dry-run --set-exit-if-changed lib/", cwd="frontend", description="Formato de código"):
        passed_tests += 1
    total_tests += 1
    
    # Flutter Tests
    print_colored("🧪 Ejecutando tests unitarios...", 'cyan')
    if run_command("flutter test", cwd="frontend", description="Tests unitarios"):
        passed_tests += 1
    total_tests += 1
    
    # Verificar dependencias actualizadas
    print_colored("📦 Verificando dependencias...", 'cyan')
    if run_command("flutter pub deps", cwd="frontend", description="Dependencias"):
        passed_tests += 1
    total_tests += 1
    
    # TypeScript compilation para Functions
    if Path("backend/functions").exists():
        print_colored("⚡ Compilando TypeScript Functions...", 'cyan')
        if run_command("npm run build", cwd="backend/functions", description="Compilación TypeScript"):
            passed_tests += 1
        total_tests += 1
    
    # Resultados finales
    print()
    print_colored("=" * 50, 'white')
    print_colored(f"📊 Resultados de Testing", 'cyan')
    print_colored(f"✅ Tests pasados: {passed_tests}/{total_tests}", 'green' if passed_tests == total_tests else 'yellow')
    
    if passed_tests == total_tests:
        print_colored("🎉 ¡Todos los tests pasaron!", 'green')
        return 0
    else:
        print_colored(f"⚠️ {total_tests - passed_tests} test(s) fallaron", 'yellow')
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
