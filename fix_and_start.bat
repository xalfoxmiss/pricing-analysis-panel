@echo off
echo ========================================
echo   REPARACION Y PANEL DE ANALISIS
echo ========================================
echo.

:: Verificar qué versión de Python está disponible
echo Verificando versiones de Python disponibles...

python --version 2>nul
if %errorlevel% equ 0 (
    echo Python encontrado:
    python --version
    set PYTHON_CMD=python
) else (
    echo Buscando Python 3.10...
    "C:\Program Files\Python310\python.exe" --version 2>nul
    if %errorlevel% equ 0 (
        echo Python 3.10 encontrado
        set PYTHON_CMD="C:\Program Files\Python310\python.exe"
    ) else (
        echo Buscando Python 3.13...
        "C:\Python313\python.exe" --version 2>nul
        if %errorlevel% equ 0 (
            echo Python 3.13 encontrado
            set PYTHON_CMD="C:\Python313\python.exe"
        ) else (
            echo ERROR: Python no encontrado en ubicaciones estándar
            echo Por favor, instale Python 3.11+
            pause
            exit /b 1
        )
    )
)

echo Usando: %PYTHON_CMD%

:: Crear directorio para reports si no existe
if not exist "reports" mkdir reports

:: Limpiar procesos previos
echo.
echo Cerrando procesos previos...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM streamlit.exe /T 2>nul
timeout /t 3 >nul

:: Instalar dependencias usando python -m pip
echo.
echo Instalando dependencias con python -m pip...
echo.

%PYTHON_CMD% -m pip --version 2>nul
if %errorlevel% neq 0 (
    echo Error: pip no disponible
    pause
    exit /b 1
)

echo Instalando Streamlit...
%PYTHON_CMD% -m pip install streamlit==1.40.0 --no-cache-dir --force-reinstall

echo Instalando Pandas...
%PYTHON_CMD% -m pip install pandas==2.2.3 --no-cache-dir --force-reinstall

echo Instalando lxml...
%PYTHON_CMD% -m pip install lxml==5.3.0 --no-cache-dir --force-reinstall

echo Instalando Plotly...
%PYTHON_CMD% -m pip install plotly==5.24.1 --no-cache-dir --force-reinstall

echo Instalando numpy y python-dateutil...
%PYTHON_CMD% -m pip install numpy==1.26.4 python-dateutil==2.9.0.post0 --no-cache-dir

echo.
echo ========================================
echo   INICIANDO PANEL
echo ========================================
echo.
echo   Panel disponible en: http://localhost:8502
echo   Presiona Ctrl+C para detener
echo.
echo ========================================

:: Iniciar panel en puerto 8502
%PYTHON_CMD% -m streamlit run app.py --server.port 8502 --server.headless false --server.runOnSave false

pause