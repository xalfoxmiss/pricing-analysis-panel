@echo off
echo ========================================
echo   Panel de Analisis de Precios v2.0
echo ========================================
echo.

:: Verificar Python disponible
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo Por favor, instale Python 3.11+
    pause
    exit /b 1
)

:: Crear directorio para reports si no existe
if not exist "reports" mkdir reports

:: Limpiar procesos previos
echo Deteniendo procesos Streamlit previos...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM streamlit.exe /T 2>nul
timeout /t 3 >nul

:: Instalar dependencias compatibles
echo Instalando dependencias compatibles con Python 3.11...
echo.

:: Versiones compatibles con Python 3.11
pip install streamlit==1.40.0 --no-cache-dir
pip install pandas==2.2.3 --no-cache-dir
pip install numpy==1.26.4 --no-cache-dir
pip install lxml==5.3.0 --no-cache-dir
pip install plotly==5.24.1 --no-cache-dir
pip install python-dateutil==2.9.0.post0 --no-cache-dir

echo.
echo ========================================
echo   INICIANDO PANEL
echo ========================================
echo.
echo   Panel disponible en: http://localhost:8501
echo   Presiona Ctrl+C para detener
echo.
echo ========================================

:: Iniciar panel
python -m streamlit run app.py --server.port 8501

pause