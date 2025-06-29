# 🔄 Migración de Scripts PowerShell a Python

## ✅ Scripts Convertidos

Los scripts han sido migrados de PowerShell (`.ps1`) a Python (`.py`) para mayor compatibilidad multiplataforma:

### Antes (PowerShell)
```powershell
.\scripts\setup.ps1      # Solo Windows
.\scripts\dev.ps1        # Solo Windows
```

### Después (Python)
```bash
python scripts/setup.py    # Multiplataforma
python scripts/dev.py      # Multiplataforma
python scripts/test.py     # Multiplataforma
python scripts/deploy.py   # Multiplataforma
```

## 🚀 Nuevas Características

### 1. **Scripts Helper**
- `run.bat` - Para Windows (CMD/PowerShell)
- `run.sh` - Para Unix/Linux/macOS

### 2. **Compatibilidad Universal**
- ✅ Windows (PowerShell, CMD, Git Bash)
- ✅ macOS (Terminal, Zsh, Bash)
- ✅ Linux (Bash, Zsh, Fish)
- ✅ WSL (Windows Subsystem for Linux)

### 3. **Funcionalidades Mejoradas**

#### `setup.py`
- Detección automática de dependencias
- Instalación automática de Firebase CLI
- Validación de estructura de archivos
- Mensajes de error más claros

#### `dev.py`
- Manejo de procesos en paralelo
- Monitoreo de servicios en tiempo real
- Captura de logs de ambos servicios
- Mejor manejo de Ctrl+C

#### `test.py`
- Suite completa de tests
- Análisis estático de código
- Verificación de formato
- Reporte de resultados detallado

#### `deploy.py`
- Tests pre-deploy automáticos
- Deploy por etapas con validación
- Reporte de componentes desplegados
- Obtención automática de URLs

## 📋 Uso Actualizado

### Configuración Inicial
```bash
# Windows
python scripts\setup.py
run.bat setup

# macOS/Linux
python3 scripts/setup.py
./run.sh setup
```

### Desarrollo
```bash
# Windows
python scripts\dev.py
run.bat dev

# macOS/Linux  
python3 scripts/dev.py
./run.sh dev
```

### Testing
```bash
# Windows
python scripts\test.py
run.bat test

# macOS/Linux
python3 scripts/test.py
./run.sh test
```

### Deploy
```bash
# Windows
python scripts\deploy.py
run.bat deploy

# macOS/Linux
python3 scripts/deploy.py
./run.sh deploy
```

## 🔧 Requisitos

- **Python 3.7+** (disponible en todos los sistemas)
- **Flutter SDK**
- **Node.js**
- **Firebase CLI**

## 🎯 Beneficios de la Migración

1. **Compatibilidad Universal**: Funciona en cualquier sistema operativo
2. **Mejor Manejo de Errores**: Detección y reportes más precisos
3. **Experiencia Unificada**: Misma funcionalidad en todos los sistemas
4. **Facilidad de Mantenimiento**: Código más limpio y modular
5. **Mejor Testing**: Suite de tests más completa

## 🔄 Migración Completada

- ❌ ~~scripts/setup.ps1~~ → ✅ scripts/setup.py
- ❌ ~~scripts/dev.ps1~~ → ✅ scripts/dev.py
- ➕ scripts/test.py (nuevo)
- ➕ scripts/deploy.py (nuevo)
- ➕ run.bat / run.sh (helpers)

La migración está completa y los scripts están listos para usar en cualquier sistema operativo.
