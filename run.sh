#!/bin/bash
# Ejecutar scripts Python desde Unix/Linux/macOS
# Helper multiplataforma para Historia 1.1

if [ $# -eq 0 ]; then
    echo "🚀 Revenue Recovery SaaS - Helper Unix/macOS"
    echo ""
    echo "Uso: ./run.sh [comando]"
    echo ""
    echo "📋 Comandos disponibles:"
    echo "  setup     - Configuración automática completa"
    echo "  validate  - Validar entorno de desarrollo"
    echo "  dev       - Iniciar desarrollo local"
    echo "  test      - Ejecutar tests automatizados"
    echo "  deploy    - Deploy a producción"
    echo ""
    echo "📖 Documentación: docs/HISTORIA_1_1_SETUP.md"
    exit 1
fi

case "$1" in
    setup)
        echo "🔧 Ejecutando setup automático..."
        python3 scripts/setup_improved.py
        ;;
    validate)
        echo "🔍 Validando entorno de desarrollo..."
        python3 scripts/validate_setup_improved.py
        ;;
    dev)
        echo "🚀 Iniciando desarrollo local..."
        python3 scripts/dev.py
        ;;
    test)
        echo "🧪 Ejecutando tests..."
        python3 scripts/test.py
        ;;
    deploy)
        echo "🚀 Desplegando a producción..."
        python3 scripts/deploy.py
        ;;
    *)
        echo "❌ Comando desconocido: $1"
        echo ""
        echo "📋 Comandos válidos: setup, validate, dev, test, deploy"
        echo "📖 Ayuda: ./run.sh"
        exit 1
        ;;
esac
