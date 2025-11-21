#!/usr/bin/env python3
"""
Script para ejecutar el panel localmente con configuración automática
"""

import subprocess
import sys
import os

def check_streamlit():
    """Verifica si Streamlit está instalado"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """Instala Streamlit si no está disponible"""
    print("📦 Instalando Streamlit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    print("🚀 Iniciando Panel Analizador de Precios")
    print("=" * 50)

    # Verificar si estamos en el directorio correcto
    if not os.path.exists("app.py"):
        print("❌ Error: No se encuentra app.py en el directorio actual")
        print("   Por favor, ejecuta este script desde el directorio del proyecto")
        return

    # Verificar dependencias
    if not check_streamlit():
        print("⚠️ Streamlit no está instalado. Instalando dependencias...")
        install_streamlit()
    else:
        print("✅ Streamlit ya está instalado")

    # Verificar archivos de ejemplo
    print("\n📁 Verificando archivos:")

    if os.path.exists("precios.csv"):
        print("   ✅ precios.csv (ejemplo CSV)")
    else:
        print("   ⚠️ precios.csv no encontrado (necesitarás subirlo al panel)")

    if os.path.exists("feed.xml"):
        print("   ✅ feed.xml (ejemplo XML)")
    else:
        print("   ⚠️ feed.xml no encontrado (necesitarás subirlo al panel)")

    print("\n🌐 Iniciando panel web...")
    print("   El panel estará disponible en: http://localhost:8501")
    print("   Presiona Ctrl+C para detener el servidor")
    print("=" * 50)

    # Iniciar Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n\n👋 Panel detenido. ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error al iniciar el panel: {e}")

if __name__ == "__main__":
    main()