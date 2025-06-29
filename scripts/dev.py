#!/usr/bin/env python3
"""
Script de Desarrollo - Historia 1.1
Inicia Flutter Web y Firebase Emulators en paralelo
"""

import os
import sys
import signal
import subprocess
import threading
import time
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

class ServiceRunner:
    def __init__(self):
        self.processes = []
        self.running = True
    
    def signal_handler(self, signum, frame):
        print_colored("\n🛑 Deteniendo servicios...", 'yellow')
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        self.running = False
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        print_colored("✅ Servicios detenidos", 'green')
    
    def run_service(self, name, command, cwd=None):
        """Ejecuta un servicio en un hilo separado"""
        def run():
            try:
                print_colored(f"🔄 Iniciando {name}...", 'cyan')
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                self.processes.append(process)
                
                # Leer output en tiempo real
                for line in iter(process.stdout.readline, ''):
                    if not self.running:
                        break
                    if line.strip():
                        print(f"[{name}] {line.strip()}")
                
            except Exception as e:
                print_colored(f"❌ Error en {name}: {e}", 'red')
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return thread
    
    def wait_for_services(self):
        """Espera a que los servicios estén listos"""
        print_colored("⏳ Esperando a que los servicios inicien...", 'yellow')
        time.sleep(10)  # Dar tiempo para que inicien
        
        # Verificar si los servicios están corriendo
        services_ok = True
        for process in self.processes:
            if process.poll() is not None:
                services_ok = False
                break
        
        if services_ok:
            print_colored("🎯 Servicios iniciados correctamente:", 'green')
            print_colored("📱 Flutter Web: http://localhost:3000", 'white')
            print_colored("🔥 Firebase UI: http://localhost:4000", 'white')
            print_colored("🗃️ Firestore: http://localhost:8080", 'white')
            print_colored("⚡ Functions: http://localhost:5001", 'white')
            print()
            print_colored("⚠️ Presiona Ctrl+C para detener todos los servicios", 'yellow')
        else:
            print_colored("❌ Algunos servicios fallaron al iniciar", 'red')
    
    def monitor_services(self):
        """Monitorea el estado de los servicios"""
        while self.running:
            time.sleep(5)
            failed_services = []
            
            for i, process in enumerate(self.processes):
                if process.poll() is not None:
                    service_name = "Flutter" if i == 0 else "Firebase"
                    failed_services.append(service_name)
            
            if failed_services:
                for service in failed_services:
                    print_colored(f"❌ {service} falló. Verificar configuración.", 'red')
                break

def main():
    print_colored("🛠️ Iniciando desarrollo Historia 1.1...", 'green')
    print()
    
    # Verificar que estamos en el directorio correcto
    if not Path("frontend").exists() or not Path("backend").exists():
        print_colored("❌ Ejecuta este script desde la raíz del proyecto", 'red')
        sys.exit(1)
    
    runner = ServiceRunner()
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, runner.signal_handler)
    signal.signal(signal.SIGTERM, runner.signal_handler)
    
    try:
        print_colored("🔄 Iniciando servicios en paralelo...", 'yellow')
        
        # Iniciar Flutter Web
        flutter_thread = runner.run_service(
            "Flutter",
            "flutter run -d web-server --web-port 3000",
            cwd="frontend"
        )
        
        # Iniciar Firebase Emulators
        firebase_thread = runner.run_service(
            "Firebase",
            "firebase emulators:start --only auth,firestore,functions",
            cwd="backend"
        )
        
        # Esperar a que los servicios inicien
        runner.wait_for_services()
        
        # Monitorear servicios
        runner.monitor_services()
        
    except KeyboardInterrupt:
        pass
    finally:
        runner.cleanup()

if __name__ == "__main__":
    main()
