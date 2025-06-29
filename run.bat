@echo off
REM Ejecutar scripts Python desde Windows
REM Helper multiplataforma para Historia 1.1

if "%1"=="" (
    echo 🚀 Revenue Recovery SaaS - Helper Windows
    echo.
    echo Uso: run.bat [comando]
    echo.
    echo 📋 Comandos disponibles:
    echo   setup     - Configuracion automatica completa
    echo   validate  - Validar entorno de desarrollo
    echo   dev       - Iniciar desarrollo local
    echo   test      - Ejecutar tests automatizados
    echo   deploy    - Deploy a produccion
    echo.
    echo 📖 Documentacion: docs\HISTORIA_1_1_SETUP.md
    exit /b 1
)

if "%1"=="setup" (
    echo 🔧 Ejecutando setup automatico...
    python scripts\setup_improved.py
) else if "%1"=="validate" (
    echo 🔍 Validando entorno de desarrollo...
    python scripts\validate_setup_improved.py
) else if "%1"=="dev" (
    echo 🚀 Iniciando desarrollo local...
    python scripts\dev.py
) else if "%1"=="test" (
    echo 🧪 Ejecutando tests...
    python scripts\test.py
) else if "%1"=="deploy" (
    echo 🚀 Desplegando a produccion...
    python scripts\deploy.py
) else (
    echo ❌ Comando desconocido: %1
    echo.
    echo 📋 Comandos validos: setup, validate, dev, test, deploy
    echo 📖 Ayuda: run.bat
    exit /b 1
)
