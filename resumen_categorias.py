#!/usr/bin/env python3
"""
Script para mostrar un resumen de las categorías extraídas del feed
"""

from pricing_analyzer import PricingAnalyzer

def main():
    print("Analizando categorías del feed de productos...")
    print("=" * 50)

    analyzer = PricingAnalyzer()

    # Cargar feed de productos
    with open('feed.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()

    analyzer.parse_product_feed_xml(xml_content)
    df = analyzer.feed_data

    print(f"Total productos en feed: {len(df):,}")
    print()

    # Resumen de categorías principales
    print("TEMPORADAS:")
    if 'temporada_limpia' in df.columns:
        temporadas = df['temporada_limpia'].value_counts().head(10)
        for temporada, count in temporadas.items():
            print(f"  {temporada}: {count:,} productos")
    print()

    print("TIPOS DE VEHÍCULO:")
    if 'vehiculo_final' in df.columns:
        vehiculos = df['vehiculo_final'].value_counts().head(10)
        for vehiculo, count in vehiculos.items():
            print(f"  {vehiculo}: {count:,} productos")
    print()

    print("SEGMENTOS DE CALIDAD:")
    if 'segmento_quality' in df.columns:
        quality = df['segmento_quality'].value_counts().head(10)
        for seg, count in quality.items():
            print(f"  {seg}: {count:,} productos")
    print()

    print("TOP 10 MEDIDAS más comunes:")
    if 'medida_final' in df.columns:
        medidas = df['medida_final'].value_counts().head(10)
        for medida, count in medidas.items():
            print(f"  {medida}: {count:,} productos")
    print()

    print("TOP 10 MODELOS más comunes:")
    if 'modelo_limpio' in df.columns:
        modelos = df['modelo_limpio'].value_counts().head(10)
        for modelo, count in modelos.items():
            if modelo and len(str(modelo)) > 1 and str(modelo).strip() != 'NAN':
                print(f"  {modelo}: {count:,} productos")
    print()

    print("TOP 10 MARCAS en el feed:")
    if 'brand' in df.columns:
        marcas = df['brand'].value_counts().head(10)
        for marca, count in marcas.items():
            print(f"  {marca}: {count:,} productos")

    print("\nAnálisis completado!")

if __name__ == "__main__":
    main()