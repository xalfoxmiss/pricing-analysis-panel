#!/usr/bin/env python3
"""
Script para verificar qué columnas están disponibles en el feed
"""

from pricing_analyzer import PricingAnalyzer

def main():
    print("Verificando columnas disponibles en el feed...")
    print("=" * 50)

    analyzer = PricingAnalyzer()

    # Cargar feed de productos
    with open('feed.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()

    analyzer.parse_product_feed_xml(xml_content)
    df = analyzer.feed_data

    print(f"Total productos en feed: {len(df):,}")
    print()
    print("Columnas disponibles:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")

    print()
    print("Columnas de modelos:")
    model_cols = [col for col in df.columns if 'modelo' in col.lower() or 'model' in col.lower()]
    for col in model_cols:
        print(f"  - {col}")

if __name__ == "__main__":
    main()