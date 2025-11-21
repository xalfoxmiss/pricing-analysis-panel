#!/usr/bin/env python3
"""
Script principal para ejecutar el análisis de competitividad de precios
"""

import os
import sys
import subprocess
from datetime import datetime
from pricing_analyzer import PricingAnalyzer
from report_generator import ReportGenerator

def install_required_packages():
    """Instala los paquetes Python necesarios"""
    required_packages = [
        'pandas',
        'numpy',
        'lxml'
    ]

    print("Verificando e instalando paquetes necesarios...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"OK: {package} ya esta instalado")
        except ImportError:
            print(f"Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """Funcion principal del analisis"""
    try:
        print("Iniciando analisis de competitividad de precios...")
        print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Instalar dependencias
        install_required_packages()

        # Verificar archivos de entrada
        precios_file = "precios.csv"
        feed_file = "feed.xml"

        if not os.path.exists(precios_file):
            print(f"Error: No se encuentra el archivo '{precios_file}'")
            print("   Asegurate de que el archivo CSV de competitividad este en el mismo directorio")
            return

        if not os.path.exists(feed_file):
            print(f"Error: No se encuentra el archivo '{feed_file}'")
            print("   Asegurate de que el feed de productos XML este en el mismo directorio")
            return

        print(f"Archivos encontrados:")
        print(f"   - Competitividad: {precios_file}")
        print(f"   - Feed productos: {feed_file}")

        # Inicializar analizador
        print("\nInicializando analizador de precios...")
        analyzer = PricingAnalyzer()

        # Cargar datos
        print("Cargando CSV de competitividad...")
        with open(precios_file, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        analyzer.parse_competitiveness_csv(csv_content)

        print("Cargando feed de productos...")
        with open(feed_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        analyzer.parse_product_feed_xml(xml_content)

        # Enriquecer datos
        print("Enriqueciendo datos...")
        enriched_data = analyzer.enrich_data()

        # Calcular metricas
        print("Calculando metricas de pricing...")
        metrics = analyzer.calculate_metrics()

        # Generar informe
        print("Generando informe HTML...")
        generator = ReportGenerator()
        html_report = generator.generate_html_report(
            metrics,
            analyzer.date_range,
            enriched_data
        )

        # Guardar informe
        timestamp = datetime.now().strftime("%Y-%m-%d")
        report_filename = f"informe_competitividad_precios_{timestamp}.html"

        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_report)

        print("\nAnalisis completado con exito!")
        print("=" * 60)
        print(f"Informe generado: {report_filename}")
        print(f"Productos analizados: {metrics['globales']['total_productos']:,}")
        print(f"Clics totales: {metrics['globales']['total_clicks']:,}")
        print(f"Calidad de datos: {metrics['calidad_datos']['porcentaje_match']:.1f}%")

        # Abrir informe en navegador (opcional)
        try:
            import webbrowser
            print(f"\nAbriendo informe en navegador...")
            webbrowser.open(f"file://{os.path.abspath(report_filename)}")
        except:
            print(f"\nPara ver el informe, abre el archivo '{report_filename}' en tu navegador")

        # Resumen ejecutivo en consola
        print("\nRESUMEN EJECUTIVO:")
        print("-" * 40)

        segments = metrics['globales']['segmento_distribucion']
        baratos_pct = segments.get('MUCHO_MAS_BARATO', 0) + segments.get('BARATO', 0)
        caros_pct = segments.get('CARO', 0) + segments.get('MUCHO_MAS_CARO', 0)

        print(f"• Posicion global: {baratos_pct:.1f}% mas baratos vs {caros_pct:.1f}% mas caros")
        print(f"• Diferencia media ponderada: {metrics['globales']['price_diff_stats']['media_ponderada']:+.2f}%")
        print(f"• Productos de riesgo: {len(metrics['productos_riesgo'])}")
        print(f"• Oportunidades identificadas: {len(metrics['oportunidades'])}")

        if metrics['marcas'] is not None and len(metrics['marcas']) > 0:
            top_brand = metrics['marcas'].iloc[0]
            print(f"• Marca principal: {top_brand['marca']} ({top_brand['clics_totales']:,} clics)")

        print("\nListo para tomar decisiones de pricing!")

    except Exception as e:
        try:
            print(f"\nError durante el analisis: {str(e)}")
        except:
            print("\nError durante el analisis - revisa los archivos de entrada")
        print("Por favor, revisa los archivos de entrada y vuelve a intentarlo.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()