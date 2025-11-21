#!/usr/bin/env python3
"""
Panel Web para Análisis de Competitividad de Precios
Streamlit MVP - Upload de archivos y generación de informes automáticos
"""

import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime
import base64

# Importar nuestras clases de análisis
from pricing_analyzer import PricingAnalyzer
from report_generator import ReportGenerator

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Precios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin-bottom: 1rem;
    }

    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }

    .warning-box {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }

    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }

    .kpi-label {
        color: #6c757d;
        font-size: 0.9rem;
    }

    .price-positive { color: #28a745; font-weight: bold; }
    .price-negative { color: #dc3545; font-weight: bold; }
    .price-neutral { color: #6c757d; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>📊 Analizador de Competitividad de Precios</h1>
        <h2>Panel Automatizado de Análisis</h2>
        <p>Sube tus archivos y genera informes de pricing en segundos</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar con instrucciones
    with st.sidebar:
        st.header("📋 Instrucciones")

        st.markdown("""
        ### 📁 Archivos necesarios:

        1. **Archivo A**: CSV de competitividad de Google Merchant Center
        2. **Archivo B**: XML de feed de productos

        ### 📋 Formato esperado:

        **CSV de Competitividad:**
        - Línea 1: Título del informe
        - Línea 2: Rango de fechas
        - Línea 3+: Cabeceras y datos

        **XML de Productos:**
        - Formato RSS con namespace Google Shopping
        - Campos: g:id, g:brand, g:product_detail, etc.
        """)

        st.markdown("---")

        st.markdown("""
        ### 🚀 Deployment:

        **Streamlit Cloud (Gratis):**
        ```bash
        pip install streamlit
        streamlit run app.py
        ```

        **O alternativas:**
        - Railway.app
        - Render.com
        - Heroku (con tier gratuito)
        """)

    # Área principal de upload
    st.header("📤 Sube tus archivos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="upload-section">
            <h3>📄 Archivo A: CSV Competitividad</h3>
            <p>Exportado de Google Merchant Center</p>
        </div>
        """, unsafe_allow_html=True)

        csv_file = st.file_uploader(
            "Arrastra tu CSV aquí o haz clic para seleccionar",
            type=['csv'],
            key="csv_upload",
            help="CSV con datos de competitividad de precios"
        )

        if csv_file:
            st.success(f"✅ CSV cargado: {csv_file.name}")

            # Vista previa del CSV
            with st.expander("📊 Vista previa del CSV"):
                try:
                    # Leer primeras líneas para detectar formato
                    content = csv_file.read()
                    csv_file.seek(0)

                    lines = content.decode('utf-8').split('\n')
                    st.write(f"**Línea 1 (Título):** {lines[0][:100]}...")
                    st.write(f"**Línea 2 (Fechas):** {lines[1][:100]}...")
                    st.write(f"**Total de líneas:** {len(lines)}")

                    # Mostrar muestra de datos
                    csv_data = '\n'.join(lines[2:10])  # Primeros 8 registros
                    df_preview = pd.read_csv(io.StringIO(csv_data))
                    st.dataframe(df_preview.head(5))

                except Exception as e:
                    st.error(f"❌ Error al leer CSV: {str(e)}")

    with col2:
        st.markdown("""
        <div class="upload-section">
            <h3>📄 Archivo B: XML Productos</h3>
            <p>Feed de productos Google Shopping</p>
        </div>
        """, unsafe_allow_html=True)

        xml_file = st.file_uploader(
            "Arrastra tu XML aquí o haz clic para seleccionar",
            type=['xml'],
            key="xml_upload",
            help="XML con feed de productos"
        )

        if xml_file:
            st.success(f"✅ XML cargado: {xml_file.name}")

            # Vista previa del XML
            with st.expander("📊 Vista previa del XML"):
                try:
                    content = xml_file.read()
                    xml_file.seek(0)

                    # Analizar estructura básica
                    xml_str = content.decode('utf-8')
                    lines = xml_str.split('\n')

                    st.write(f"**Total de líneas:** {len(lines)}")
                    st.write(f"**Primera línea:** {lines[0]}")

                    # Buscar items
                    item_count = xml_str.count('<item>')
                    st.write(f"**Items encontrados:** {item_count:,}")

                    # Mostrar muestra de estructura
                    if len(lines) > 10:
                        st.code('\n'.join(lines[1:15]), language='xml')

                except Exception as e:
                    st.error(f"❌ Error al leer XML: {str(e)}")

    # Botón de procesamiento
    st.markdown("---")

    if csv_file and xml_file:
        st.header("🚀 Procesar Análisis")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("📊 GENERAR INFORME", type="primary", use_container_width=True):
                with st.spinner("🔄 Procesando datos... Esto puede tardar unos segundos"):
                    try:
                        # Leer archivos
                        csv_content = csv_file.read().decode('utf-8')
                        xml_content = xml_file.read().decode('utf-8')

                        # Ejecutar análisis
                        analyzer = PricingAnalyzer()

                        # Paso 1: Parsear CSV
                        analyzer.parse_competitiveness_csv(csv_content)

                        # Paso 2: Parsear XML
                        analyzer.parse_product_feed_xml(xml_content)

                        # Paso 3: Enriquecer datos
                        enriched_data = analyzer.enrich_data()

                        # Paso 4: Calcular métricas
                        metrics = analyzer.calculate_metrics()

                        # Paso 5: Generar informe HTML
                        generator = ReportGenerator()
                        html_report = generator.generate_html_report(
                            metrics,
                            analyzer.date_range,
                            enriched_data
                        )

                        # Éxito del procesamiento
                        st.success("✅ ¡Análisis completado con éxito!")

                        # Mostrar resumen ejecutivo
                        st.header("📈 Resumen Ejecutivo")

                        # KPIs principales
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-value">{metrics['globales']['total_productos']:,}</div>
                                <div class="kpi-label">Productos Analizados</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-value">{metrics['globales']['total_clicks']:,}</div>
                                <div class="kpi-label">Clics Totales</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col3:
                            price_diff = metrics['globales']['price_diff_stats']['media_ponderada']
                            price_class = "price-positive" if price_diff < -1 else "price-negative" if price_diff > 1 else "price-neutral"
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-value {price_class}">{price_diff:+.2f}%</div>
                                <div class="kpi-label">Diff. Precio Media</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col4:
                            quality_pct = metrics['calidad_datos']['porcentaje_match']
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-value">{quality_pct:.1f}%</div>
                                <div class="kpi-label">Calidad de Datos</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Métricas clave
                        st.header("🎯 Métricas Clave")

                        col1, col2 = st.columns(2)

                        with col1:
                            segments = metrics['globales']['segmento_distribucion']
                            baratos_pct = segments.get('MUCHO_MAS_BARATO', 0) + segments.get('BARATO', 0)
                            caros_pct = segments.get('CARO', 0) + segments.get('MUCHO_MAS_CARO', 0)

                            st.metric("📉 Posición Global",
                                    f"{baratos_pct:.1f}% más baratos vs {caros_pct:.1f}% más caros")
                            st.metric("⚠️ Productos de Riesgo",
                                    f"{len(metrics['productos_riesgo'])}")
                            st.metric("💰 Oportunidades",
                                    f"{len(metrics['oportunidades'])}")

                        with col2:
                            if metrics['marcas'] is not None and len(metrics['marcas']) > 0:
                                top_brand = metrics['marcas'].iloc[0]
                                st.metric("🏆 Marca Principal",
                                        f"{top_brand['marca']} ({top_brand['clics_totales']:,} clics)")

                            if metrics['temporadas'] is not None and len(metrics['temporadas']) > 0:
                                top_temporada = metrics['temporadas'].iloc[0]
                                st.metric("🌤️ Temporada Principal",
                                        f"{top_temporada['temporada']} ({top_temporada['clics_totales']:,} clics)")

                        # Descarga del informe
                        st.header("📥 Descargar Informe Completo")

                        # Crear enlace de descarga
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"informe_competitividad_{timestamp}.html"

                        st.markdown(f"""
                        <div class="success-box">
                            <h4>📋 Informe HTML generado: {filename}</h4>
                            <p>✅ Incluye análisis completo por marcas, medidas, temporadas y vehículos</p>
                            <p>✅ Tablas interactivas y gráficos dinámicos</p>
                            <p>✅ Recomendaciones accionables y conclusiones clave</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Botón de descarga
                        b64 = base64.b64encode(html_report.encode()).decode()
                        href = f'<a href="data:file/html;base64,{b64}" download="{filename}">📥 DESCARGAR INFORME HTML</a>'
                        st.markdown(href, unsafe_allow_html=True)

                        # Vista previa del informe
                        with st.expander("👁️ Vista previa del informe HTML"):
                            st.components.v1.html(html_report, height=600, scrolling=True)

                    except Exception as e:
                        st.error(f"❌ Error en el procesamiento: {str(e)}")
                        st.error("Por favor, verifica que los archivos tengan el formato correcto.")
                        import traceback
                        st.error("Detalles técnicos:")
                        st.code(traceback.format_exc())

    else:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Esperando archivos...</h4>
            <p>Por favor, sube ambos archivos (CSV y XML) para comenzar el análisis.</p>
            <p>Los archivos deben tener el formato esperado para un procesamiento correcto.</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 20px;">
        <p>🚀 Panel MVP v1.0 | Desarrollado con Streamlit | Desarrollado por <a href="https://www.alfonsocalero.es/" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">Alfonso Calero</a></p>
        <p>💡 Para deployment: pip install streamlit && streamlit run app.py</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()