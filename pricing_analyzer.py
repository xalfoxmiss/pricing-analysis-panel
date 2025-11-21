#!/usr/bin/env python3
"""
Analizador de competitividad de precios para Muchoneumatico.com
Procesa datos de Google Merchant Center y feed de productos para generar informes
"""

import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PricingAnalyzer:
    def __init__(self):
        self.competitiveness_data = None
        self.feed_data = None
        self.enriched_data = None
        self.date_range = None

    def parse_competitiveness_csv(self, csv_content: str) -> pd.DataFrame:
        """
        Parsea el CSV de competitividad de Google Merchant Center
        """
        import io

        lines = csv_content.strip().split('\n')

        # Extraer rango de fechas de la segunda línea
        date_line = lines[1].strip('"')
        self.date_range = date_line

        # Parsear CSV a partir de la tercera línea
        csv_data = '\n'.join(lines[2:])

        # Usar io.StringIO para leer el CSV
        df = pd.read_csv(io.StringIO(csv_data))

        # Limpiar y tipificar columnas
        df['Tu precio'] = pd.to_numeric(df['Tu precio'], errors='coerce')
        df['Referencia'] = pd.to_numeric(df['Referencia'], errors='coerce')
        df['Diferencia de precios'] = pd.to_numeric(df['Diferencia de precios'], errors='coerce')
        df['Clics'] = pd.to_numeric(df['Clics'], errors='coerce')

        # Crear columna de diferencia en porcentaje
        df['price_diff_pct'] = df['Diferencia de precios'] * 100

        # Crear segmento de precio
        df['segmento_precio'] = df['price_diff_pct'].apply(self._get_price_segment)

        self.competitiveness_data = df
        print(f"CSV de competitividad cargado: {len(df)} productos")
        return df

    def parse_product_feed_xml(self, xml_content: str) -> pd.DataFrame:
        """
        Parsea el feed de productos en formato XML
        """
        # Registrar el namespace de Google Shopping
        ns = {'g': 'http://base.google.com/ns/1.0'}
        root = ET.fromstring(xml_content)

        products = []
        for item in root.findall('.//item'):
            product = {}

            # Campos estándar de Google Shopping usando namespace
            product['product_id'] = self._get_xml_text_with_ns(item, 'g:id', ns)
            product['title'] = self._get_xml_text_with_ns(item, 'g:title', ns)
            product['description'] = self._get_xml_text_with_ns(item, 'g:description', ns)
            product['link'] = self._get_xml_text_with_ns(item, 'g:link', ns)
            product['image_link'] = self._get_xml_text_with_ns(item, 'g:image_link', ns)
            product['availability'] = self._get_xml_text_with_ns(item, 'g:availability', ns)
            product['price'] = self._get_xml_text_with_ns(item, 'g:price', ns)
            product['sale_price'] = self._get_xml_text_with_ns(item, 'g:sale_price', ns)
            product['brand'] = self._get_xml_text_with_ns(item, 'g:brand', ns)
            product['gtin'] = self._get_xml_text_with_ns(item, 'g:gtin', ns)
            product['mpn'] = self._get_xml_text_with_ns(item, 'g:mpn', ns)

            # Extraer información adicional de product_detail
            product_details = item.findall('.//g:product_detail', ns)
            for detail in product_details:
                section_name = self._get_xml_text_with_ns(detail, 'g:section_name', ns)
                attribute_name = self._get_xml_text_with_ns(detail, 'g:attribute_name', ns)
                attribute_value = self._get_xml_text_with_ns(detail, 'g:attribute_value', ns)

                if attribute_name and attribute_value:
                    # Guardar información estructurada por sección y atributo
                    if section_name:
                        product[f'section_{section_name.lower()}_{attribute_name.lower()}'] = attribute_value
                    else:
                        product[f'attribute_{attribute_name.lower()}'] = attribute_value

            # Extraer custom labels
            product['custom_label_2'] = self._get_xml_text_with_ns(item, 'g:custom_label_2', ns)
            product['custom_label_3'] = self._get_xml_text_with_ns(item, 'g:custom_label_3', ns)
            product['custom_label_4'] = self._get_xml_text_with_ns(item, 'g:custom_label_4', ns)
            product['custom_label_5'] = self._get_xml_text_with_ns(item, 'g:custom_label_5', ns)

            # Extraer dimensions y pattern
            product['dimensions'] = self._get_xml_text_with_ns(item, 'g:dimensions', ns)
            product['pattern'] = self._get_xml_text_with_ns(item, 'g:pattern', ns)

            # Intentar extraer categorías del título
            if product['title']:
                product['category_inferred'] = self._infer_category_from_title(product['title'])
                product['vehicle_type'] = self._infer_vehicle_type(product['title'])
                product['season'] = self._infer_season(product['title'])

            # Limpiar precios
            for price_field in ['price', 'sale_price']:
                if product[price_field]:
                    product[f'{price_field}_num'] = self._extract_price(product[price_field])
                    product[f'{price_field}_currency'] = self._extract_currency(product[price_field])

            products.append(product)

        df = pd.DataFrame(products)

        # Estandarizar marcas
        df['brand_standardized'] = df['brand'].str.strip().str.upper() if 'brand' in df.columns else None

        # Estandarizar categorías adicionales
        if 'section_general_medida' in df.columns:
            df['medida_limpia'] = df['section_general_medida'].str.strip().str.upper()
        if 'section_general_modelo' in df.columns:
            df['modelo_limpio'] = df['section_general_modelo'].str.strip().str.upper()
        if 'section_general_temporada' in df.columns:
            df['temporada_limpia'] = df['section_general_temporada'].str.strip().str.title()
        if 'section_general_vehículo' in df.columns:
            df['vehiculo_limpio'] = df['section_general_vehículo'].str.strip().str.title()
        if 'custom_label_2' in df.columns:
            df['vehiculo_custom'] = df['custom_label_2'].str.strip().str.title()
        if 'custom_label_3' in df.columns:
            df['segmento_quality'] = df['custom_label_3'].str.strip().str.upper()
        if 'dimensions' in df.columns:
            df['medida_dimensions'] = df['dimensions'].str.strip().str.upper()

        # Unificar medidas de diferentes fuentes
        if 'medida_limpia' in df.columns and 'medida_dimensions' in df.columns:
            df['medida_final'] = df['medida_limpia'].fillna(df['medida_dimensions'])
        elif 'medida_limpia' in df.columns:
            df['medida_final'] = df['medida_limpia']
        elif 'medida_dimensions' in df.columns:
            df['medida_final'] = df['medida_dimensions']

        # Unificar vehículo de diferentes fuentes
        if 'vehiculo_limpio' in df.columns and 'vehiculo_custom' in df.columns:
            df['vehiculo_final'] = df['vehiculo_limpio'].fillna(df['vehiculo_custom'])
        elif 'vehiculo_limpio' in df.columns:
            df['vehiculo_final'] = df['vehiculo_limpio']
        elif 'vehiculo_custom' in df.columns:
            df['vehiculo_final'] = df['vehiculo_custom']

        self.feed_data = df
        print(f"Feed de productos cargado: {len(df)} productos")
        return df

    def enrich_data(self) -> pd.DataFrame:
        """
        Enriquece los datos de competitividad con información del feed
        Compatible con múltiples formatos de feeds
        """
        if self.competitiveness_data is None or self.feed_data is None:
            raise ValueError("Debes cargar ambos datasets antes de enriquecer")

        # Detectar columnas de ID en ambos datasets
        comp_id_col = self._detect_id_column(self.competitiveness_data)
        feed_id_col = self._detect_id_column(self.feed_data)

        print(f"Columnas de ID detectadas: CSV='{comp_id_col}', Feed='{feed_id_col}'")

        # Preparar datos para merge robusto
        comp_data = self.competitiveness_data.copy()
        feed_data = self.feed_data.copy()

        # Convertir IDs a string para comparación
        comp_data['_merge_key'] = comp_data[comp_id_col].astype(str).str.strip().str.upper()
        feed_data['_merge_key'] = feed_data[feed_id_col].astype(str).str.strip().str.upper()

        # Merge usando claves estandarizadas
        merged = comp_data.merge(
            feed_data.drop(columns=[feed_id_col]),  # Eliminar columna original del feed
            left_on='_merge_key',
            right_on='_merge_key',
            how='left',
            suffixes=('_merchant', '_feed')
        )

        # Limpiar columna temporal
        merged.drop(columns=['_merge_key'], inplace=True)

        # Estandarizar marcas
        merged['marca_final'] = merged['Marca'].str.strip().str.upper()

        # Métricas adicionales
        merged['impacto_clicks'] = merged['Clics'] * abs(merged['price_diff_pct'])
        merged['precio_ajustado'] = merged['Tu precio'] * (1 + merged['Diferencia de precios'])

        self.enriched_data = merged
        print(f"Datos enriquecidos: {len(merged)} productos con match")

        # Reportar calidad de datos
        if 'product_id_feed' in merged.columns:
            unmatched = len(merged[merged['product_id_feed'].isna()])
        else:
            unmatched = len(merged[merged['title_feed'].isna()])

        total = len(self.competitiveness_data)
        print(f"Productos sin match en feed: {unmatched}/{total} ({unmatched/total*100:.1f}%)")

        return merged

    def _detect_id_column(self, df: pd.DataFrame) -> str:
        """
        Detecta automáticamente la columna de ID en el dataframe
        Compatible con múltiples formatos de feeds
        """
        # Lista de posibles nombres de columnas de ID
        id_columns = [
            'id', 'ID', 'product_id', 'product-id', 'productId',
            'sku', 'SKU', 'item_id', 'item-id', 'itemId',
            'ID de producto', 'ID producto', 'product code',
            'g:id', 'identifier', 'reference', 'ref'
        ]

        # Buscar columnas exactas
        for col in df.columns:
            for id_col in id_columns:
                if col.lower().strip() == id_col.lower().strip():
                    print(f"Columna ID detectada: '{col}'")
                    return col

        # Buscar columnas que contienen palabras clave
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in ['id', 'sku', 'codigo', 'code', 'ref']):
                # Verificar que tenga datos únicos (característica de ID)
                unique_ratio = df[col].nunique() / len(df[col])
                if unique_ratio > 0.8:  # Muy probable que sea un ID
                    print(f"Columna ID detectada por patrón: '{col}' (ratio: {unique_ratio:.2f})")
                    return col

        # Si no se encuentra, usar la primera columna
        first_col = df.columns[0]
        print(f"Columna ID no detectada, usando primera columna: '{first_col}'")
        return first_col

    def calculate_metrics(self) -> Dict:
        """
        Calcula métricas clave de pricing
        """
        if self.enriched_data is None:
            raise ValueError("Debes enriquecer los datos primero")

        df = self.enriched_data.copy()

        # Métricas globales
        total_clicks = df['Clics'].sum()
        total_products = len(df)

        # Distribución por segmento de precio
        segment_dist = df.groupby('segmento_precio')['Clics'].sum()
        segment_pct = (segment_dist / total_clicks * 100).round(1)

        # Métricas de precio
        price_diff_stats = {
            'media_simple': df['price_diff_pct'].mean(),
            'mediana': df['price_diff_pct'].median(),
            'media_ponderada': (df['price_diff_pct'] * df['Clics']).sum() / total_clicks
        }

        # Análisis por marca
        brand_metrics = []
        for brand in df['Marca'].unique():
            brand_data = df[df['Marca'] == brand]
            brand_clicks = brand_data['Clics'].sum()

            if brand_clicks > 0:
                brand_segment_dist = brand_data.groupby('segmento_precio')['Clics'].sum()
                brand_segment_pct = (brand_segment_dist / brand_clicks * 100).round(1)

                brand_metrics.append({
                    'marca': brand,
                    'clics_totales': brand_clicks,
                    'productos': len(brand_data),
                    'price_diff_media_simple': brand_data['price_diff_pct'].mean(),
                    'price_diff_media_ponderada': (brand_data['price_diff_pct'] * brand_data['Clics']).sum() / brand_clicks,
                    'segmentos': brand_segment_pct.to_dict()
                })

        # Convertir a DataFrame y ordenar
        brand_df = pd.DataFrame(brand_metrics).sort_values('clics_totales', ascending=False)

        # Análisis por categoría si existe
        category_metrics = None
        if 'category_inferred' in df.columns:
            category_metrics = []
            for category in df['category_inferred'].dropna().unique():
                cat_data = df[df['category_inferred'] == category]
                cat_clicks = cat_data['Clics'].sum()

                if cat_clicks > 0:
                    category_metrics.append({
                        'categoria': category,
                        'clics_totales': cat_clicks,
                        'productos': len(cat_data),
                        'price_diff_media_ponderada': (cat_data['price_diff_pct'] * cat_data['Clics']).sum() / cat_clicks
                    })

            category_df = pd.DataFrame(category_metrics).sort_values('clics_totales', ascending=False)
        else:
            category_df = None

        # Análisis por medidas
        medida_metrics = []
        if 'medida_final' in df.columns:
            for medida in df['medida_final'].dropna().unique():
                if len(str(medida)) > 3:  # Ignorar medidas vacías o muy cortas
                    medida_data = df[df['medida_final'] == medida]
                    medida_clicks = medida_data['Clics'].sum()

                    if medida_clicks > 50:  # Solo medidas con clics significativos
                        medida_metrics.append({
                            'medida': medida,
                            'clics_totales': medida_clicks,
                            'productos': len(medida_data),
                            'price_diff_media_ponderada': (medida_data['price_diff_pct'] * medida_data['Clics']).sum() / medida_clicks
                        })

            medida_df = pd.DataFrame(medida_metrics).sort_values('clics_totales', ascending=False)
        else:
            medida_df = None

        # Análisis por modelos
        modelo_metrics = []
        if 'modelo_limpio' in df.columns:
            for modelo in df['modelo_limpio'].dropna().unique():
                if len(str(modelo)) > 1:  # Ignorar modelos vacíos
                    modelo_data = df[df['modelo_limpio'] == modelo]
                    modelo_clicks = modelo_data['Clics'].sum()

                    if modelo_clicks > 30:  # Solo modelos con clics significativos
                        modelo_metrics.append({
                            'modelo': modelo,
                            'clics_totales': modelo_clicks,
                            'productos': len(modelo_data),
                            'price_diff_media_ponderada': (modelo_data['price_diff_pct'] * modelo_data['Clics']).sum() / modelo_clicks
                        })

            modelo_df = pd.DataFrame(modelo_metrics).sort_values('clics_totales', ascending=False)
        else:
            modelo_df = None

        # Análisis por temporadas
        temporada_metrics = []
        if 'temporada_limpia' in df.columns:
            for temporada in df['temporada_limpia'].dropna().unique():
                if len(str(temporada)) > 2:  # Ignorar temporadas vacías
                    temporada_data = df[df['temporada_limpia'] == temporada]
                    temporada_clicks = temporada_data['Clics'].sum()

                    if temporada_clicks > 0:
                        temporada_metrics.append({
                            'temporada': temporada,
                            'clics_totales': temporada_clicks,
                            'productos': len(temporada_data),
                            'price_diff_media_ponderada': (temporada_data['price_diff_pct'] * temporada_data['Clics']).sum() / temporada_clicks
                        })

            temporada_df = pd.DataFrame(temporada_metrics).sort_values('clics_totales', ascending=False)
        else:
            temporada_df = None

        # Análisis por vehículo
        vehiculo_metrics = []
        if 'vehiculo_final' in df.columns:
            for vehiculo in df['vehiculo_final'].dropna().unique():
                if len(str(vehiculo)) > 2:  # Ignorar vehículos vacíos
                    vehiculo_data = df[df['vehiculo_final'] == vehiculo]
                    vehiculo_clicks = vehiculo_data['Clics'].sum()

                    if vehiculo_clicks > 0:
                        vehiculo_metrics.append({
                            'vehiculo': vehiculo,
                            'clics_totales': vehiculo_clicks,
                            'productos': len(vehiculo_data),
                            'price_diff_media_ponderada': (vehiculo_data['price_diff_pct'] * vehiculo_data['Clics']).sum() / vehiculo_clicks
                        })

            vehiculo_df = pd.DataFrame(vehiculo_metrics).sort_values('clics_totales', ascending=False)
        else:
            vehiculo_df = None

        # Análisis por segmento de calidad
        quality_metrics = []
        if 'segmento_quality' in df.columns:
            for quality in df['segmento_quality'].dropna().unique():
                if len(str(quality)) > 1:  # Ignorar segmentos vacíos
                    quality_data = df[df['segmento_quality'] == quality]
                    quality_clicks = quality_data['Clics'].sum()

                    if quality_clicks > 0:
                        quality_metrics.append({
                            'quality': quality,
                            'clics_totales': quality_clicks,
                            'productos': len(quality_data),
                            'price_diff_media_ponderada': (quality_data['price_diff_pct'] * quality_data['Clics']).sum() / quality_clicks
                        })

            quality_df = pd.DataFrame(quality_metrics).sort_values('clics_totales', ascending=False)
        else:
            quality_df = None

        # Top productos
        top_products = df.nlargest(50, 'Clics')

        # Productos de riesgo (caros con muchos clics)
        clicks_threshold = df['Clics'].quantile(0.75)
        risk_products = df[(df['price_diff_pct'] > 0) & (df['Clics'] > clicks_threshold)]
        risk_products = risk_products.nlargest(20, ['price_diff_pct', 'Clics'])

        # Oportunidades (baratos con muchos clics)
        opportunity_products = df[(df['price_diff_pct'] < 0) & (df['Clics'] > clicks_threshold)]
        opportunity_products = opportunity_products.nlargest(20, ['Clics', 'price_diff_pct'])

        # Calidad de datos
        data_quality = {
            'total_productos_csv': len(self.competitiveness_data),
            'total_productos_feed': len(self.feed_data),
            'productos_con_match': len(df[df['product_id'].notna()]),
            'productos_sin_match': len(df[df['product_id'].isna()]),
            'porcentaje_match': len(df[df['product_id'].notna()]) / len(self.competitiveness_data) * 100,
            'clics_con_match': df[df['product_id'].notna()]['Clics'].sum(),
            'clics_sin_match': df[df['product_id'].isna()]['Clics'].sum()
        }

        return {
            'globales': {
                'total_clicks': total_clicks,
                'total_productos': total_products,
                'segmento_distribucion': segment_pct.to_dict(),
                'price_diff_stats': price_diff_stats
            },
            'marcas': brand_df,
            'categorias': category_df,
            'medidas': medida_df,
            'modelos': modelo_df,
            'temporadas': temporada_df,
            'vehiculos': vehiculo_df,
            'quality_segments': quality_df,
            'top_productos': top_products,
            'productos_riesgo': risk_products,
            'oportunidades': opportunity_products,
            'calidad_datos': data_quality
        }

    def _get_price_segment(self, diff_pct: float) -> str:
        """Clasifica el producto según su diferencia de precio"""
        if diff_pct <= -5:
            return 'MUCHO_MAS_BARATO'
        elif diff_pct <= -1:
            return 'BARATO'
        elif diff_pct < 1:
            return 'ALINEADO'
        elif diff_pct < 5:
            return 'CARO'
        else:
            return 'MUCHO_MAS_CARO'

    def _get_xml_text(self, element, tag: str) -> str:
        """Extrae texto de un elemento XML de forma segura"""
        found = element.find(f'.//{tag}')
        return found.text if found is not None else ''

    def _get_xml_text_with_ns(self, element, tag: str, ns: dict) -> str:
        """Extrae texto de un elemento XML con namespace de forma segura"""
        found = element.find(f'.//{tag}', ns)
        return found.text if found is not None else ''

    def _extract_price(self, price_str: str) -> float:
        """Extrae valor numérico de un string de precio"""
        if not price_str:
            return None
        # Buscar números con decimales
        match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', '.'))
        return float(match.group()) if match else None

    def _extract_currency(self, price_str: str) -> str:
        """Extrae moneda de un string de precio"""
        if not price_str:
            return None
        match = re.search(r'[A-Z]{3}', price_str.upper())
        return match.group() if match else None

    def _infer_category_from_title(self, title: str) -> str:
        """Infiere categoría del título del producto"""
        title_lower = title.lower()

        if any(word in title_lower for word in ['turismo', 'touring', 'passenger']):
            return 'turismo'
        elif any(word in title_lower for word in ['4x4', 'suv', '4x2', 'off-road', 'all terrain']):
            return '4x4'
        elif any(word in title_lower for word in ['furgoneta', 'van', 'camion', 'cargo']):
            return 'furgoneta'
        elif any(word in title_lower for word in ['moto', 'motorcycle']):
            return 'moto'
        else:
            return 'otro'

    def _infer_vehicle_type(self, title: str) -> str:
        """Infiere tipo de vehículo del título"""
        title_lower = title.lower()

        if 'coche' in title_lower or 'turismo' in title_lower:
            return 'coche'
        elif any(word in title_lower for word in ['suv', '4x4']):
            return 'suv'
        elif 'furgoneta' in title_lower:
            return 'furgoneta'
        else:
            return 'desconocido'

    def _infer_season(self, title: str) -> str:
        """Infiere temporada del neumático del título"""
        title_lower = title.lower()

        if 'invierno' in title_lower or 'winter' in title_lower:
            return 'invierno'
        elif 'verano' in title_lower or 'summer' in title_lower:
            return 'verano'
        elif any(word in title_lower for word in ['all season', '4 estaciones']):
            return 'all_season'
        else:
            return 'desconocida'

if __name__ == "__main__":
    analyzer = PricingAnalyzer()
    print("Analizador de precios inicializado correctamente")