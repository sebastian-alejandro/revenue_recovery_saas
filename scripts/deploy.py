#!/usr/bin/env python3
"""
Script de Deploy - Historia 1.1
Construye y despliega la aplicación a Firebase
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
            text=True
        )
        
        if result.returncode == 0:
            print_colored(f"✅ {description} - Exitoso", 'green')
            return True
        else:
            print_colored(f"❌ {description} - Falló", 'red')
            return False
            
    except Exception as e:
        print_colored(f"❌ Error ejecutando {description}: {e}", 'red')
        return False

def main():
    print_colored("🚀 Desplegando Historia 1.1...", 'green')
    print()
    
    # Verificar que estamos en el directorio correcto
    if not Path("frontend").exists() or not Path("backend").exists():
        print_colored("❌ Ejecuta este script desde la raíz del proyecto", 'red')
        sys.exit(1)
    
    # Verificar que Firebase está configurado
    if not Path("backend/firebase.json").exists():
        print_colored("❌ Firebase no está configurado. Ejecuta 'firebase init' primero.", 'red')
        sys.exit(1)
    
    deploy_steps = []
    
    # Paso 1: Ejecutar tests
    print_colored("🧪 Ejecutando tests antes del deploy...", 'cyan')
    if run_command("python scripts/test.py", description="Tests pre-deploy"):
        deploy_steps.append("Tests")
    else:
        print_colored("⚠️ Tests fallaron. ¿Continuar con el deploy? (y/N): ", 'yellow', end='')
        response = input().strip().lower()
        if response != 'y':
            print_colored("❌ Deploy cancelado", 'red')
            sys.exit(1)
    
    # Paso 2: Build Flutter Web
    print_colored("📱 Construyendo Flutter Web...", 'cyan')
    if run_command("flutter build web --release", cwd="frontend", description="Build Flutter Web"):
        deploy_steps.append("Flutter Build")
    else:
        print_colored("❌ Error en build de Flutter", 'red')
        sys.exit(1)
    
    # Paso 3: Build Functions
    print_colored("⚡ Construyendo Functions...", 'cyan')
    if run_command("npm run build", cwd="backend/functions", description="Build Functions"):
        deploy_steps.append("Functions Build")
    else:
        print_colored("❌ Error en build de Functions", 'red')
        sys.exit(1)
    
    # Paso 4: Deploy Firestore Rules
    print_colored("🔥 Desplegando reglas de Firestore...", 'cyan')
    if run_command("firebase deploy --only firestore:rules", cwd="backend", description="Deploy Firestore Rules"):
        deploy_steps.append("Firestore Rules")
    else:
        print_colored("❌ Error desplegando reglas de Firestore", 'red')
        sys.exit(1)
    
    # Paso 5: Deploy Functions
    print_colored("⚡ Desplegando Cloud Functions...", 'cyan')
    if run_command("firebase deploy --only functions", cwd="backend", description="Deploy Functions"):
        deploy_steps.append("Cloud Functions")
    else:
        print_colored("❌ Error desplegando Functions", 'red')
        sys.exit(1)
    
    # Paso 6: Deploy Hosting
    print_colored("🌐 Desplegando Hosting...", 'cyan')
    if run_command("firebase deploy --only hosting", cwd="backend", description="Deploy Hosting"):
        deploy_steps.append("Hosting")
    else:
        print_colored("❌ Error desplegando Hosting", 'red')
        sys.exit(1)
    
    # Resultados finales
    print()
    print_colored("=" * 50, 'white')
    print_colored("🎉 Deploy completado exitosamente!", 'green')
    print_colored("✅ Componentes desplegados:", 'green')
    for step in deploy_steps:
        print_colored(f"   • {step}", 'white')
    
    print()
    print_colored("🌐 Tu aplicación está disponible en:", 'cyan')
    
    # Obtener URL del proyecto
    try:
        result = subprocess.run(
            "firebase hosting:channel:list",
            shell=True,
            cwd="backend",
            capture_output=True,
            text=True
        )
        if "live" in result.stdout:
            print_colored("   https://revenue-recovery-saas.web.app", 'white')
        else:
            print_colored("   Ejecuta 'firebase hosting:channel:list' para ver la URL", 'white')
    except:
        print_colored("   Ejecuta 'firebase hosting:channel:list' para ver la URL", 'white')

if __name__ == "__main__":
    main()
