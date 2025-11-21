#!/usr/bin/env python3
"""
Generador de informes HTML para análisis de competitividad de precios
"""

import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any
import base64

class ReportGenerator:
    def __init__(self):
        self.report_date = datetime.now().strftime("%Y-%m-%d")

    def generate_html_report(self, metrics: Dict, date_range: str, enriched_data: pd.DataFrame) -> str:
        """
        Genera el informe HTML completo con todos los análisis
        """

        # Preparar datos para gráficos
        charts_data = self._prepare_charts_data(metrics)

        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Competitividad de Precios</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- DataTables CSS -->
    <link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }}

        .header-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}

        .kpi-card {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            transition: transform 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
        }}

        .kpi-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}

        .kpi-label {{
            color: #6c757d;
            font-size: 0.9rem;
        }}

        .segment-barato {{ color: #28a745; }}
        .segment-alineado {{ color: #6c757d; }}
        .segment-caro {{ color: #ffc107; }}
        .segment-muy-caro {{ color: #dc3545; }}
        .segment-muy-barato {{ color: #20c997; }}

        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        .table-container {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        .section-title {{
            color: #495057;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}

        .alert-custom {{
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}

        .data-quality {{
            background: #e9ecef;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }}

        .recommendation {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}

        .price-positive {{ color: #28a745; font-weight: bold; }}
        .price-negative {{ color: #dc3545; font-weight: bold; }}
        .price-neutral {{ color: #6c757d; font-weight: bold; }}

        @media (max-width: 768px) {{
            .kpi-value {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header-section">
        <div class="container">
            <h1 class="display-4 fw-bold">
                <i class="fas fa-chart-line me-3"></i>
                Informe de Competitividad de Precios
            </h1>
            <h2 class="h4">Desarrollado por <a href="https://www.alfonsocalero.es/" target="_blank" style="color: white; text-decoration: none;">Alfonso Calero</a></h2>
            <p class="lead mb-0">
                <i class="far fa-calendar-alt me-2"></i>
                Periodo analizado: {date_range}
            </p>
            <p class="mb-0">
                <i class="far fa-clock me-2"></i>
                Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </p>
        </div>
    </div>

    <div class="container">
        <!-- Resumen Ejecutivo -->
        <div class="alert alert-info alert-custom">
            <h5><i class="fas fa-lightbulb me-2"></i>Resumen Ejecutivo</h5>
            <div class="row">
                <div class="col-md-6">
                    <ul>
                        <li><strong>Posición global:</strong> Somos {self._get_position_summary(metrics['globales'])} en {metrics['globales']['segmento_distribucion'].get('ALINEADO', 0)}% de los clics analizados.</li>
                        <li><strong>Marcas mejor posicionadas:</strong> {self._get_top_brands_summary(metrics['marcas'])}</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <ul>
                        <li><strong>Puntos críticos:</strong> {self._get_critical_points_summary(metrics)}</li>
                        <li><strong>Oportunidades rápidas:</strong> {self._get_quick_opportunities_summary(metrics)}</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- KPIs Globales -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="kpi-card text-center">
                    <div class="kpi-value">{metrics['globales']['total_productos']:,}</div>
                    <div class="kpi-label">Productos Analizados</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card text-center">
                    <div class="kpi-value">{metrics['globales']['total_clicks']:,}</div>
                    <div class="kpi-label">Clics Totales</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card text-center">
                    <div class="kpi-value price-{self._get_price_class(metrics['globales']['price_diff_stats']['media_ponderada'])}">
                        {metrics['globales']['price_diff_stats']['media_ponderada']:+.2f}%
                    </div>
                    <div class="kpi-label">Diferencia Media Ponderada</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card text-center">
                    <div class="kpi-value">
                        {metrics['calidad_datos']['porcentaje_match']:.1f}%
                    </div>
                    <div class="kpi-label">Datos Completos</div>
                </div>
            </div>
        </div>

        <!-- Distribución por Segmento -->
        <div class="row">
            <div class="col-md-6">
                <div class="chart-container">
                    <h5 class="section-title">Distribución de Clics por Segmento de Precio</h5>
                    <canvas id="segmentChart"></canvas>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <h5 class="section-title">Dispersión Precio vs Clics</h5>
                    <canvas id="scatterChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Análisis por Marcas -->
        <div class="table-container">
            <h3 class="section-title"><i class="fas fa-tag me-2"></i>Análisis por Marcas</h3>
            <table id="brandsTable" class="table table-striped">
                <thead>
                    <tr>
                        <th>Marca</th>
                        <th>Clics</th>
                        <th>Productos</th>
                        <th>Diff. Precio Media</th>
                        <th>Diff. Precio Ponderada</th>
                        <th>Muy Baratos</th>
                        <th>Baratos</th>
                        <th>Alineados</th>
                        <th>Caros</th>
                        <th>Muy Caros</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_brands_table_rows(metrics['marcas'])}
                </tbody>
            </table>
        </div>

        <!-- Análisis por Temporadas -->
        {self._generate_temporadas_section(metrics['temporadas'])}

        <!-- Análisis por Vehículos -->
        {self._generate_vehiculos_section(metrics['vehiculos'])}

        <!-- Análisis por Segmentos de Calidad -->
        {self._generate_quality_section(metrics['quality_segments'])}

        <!-- Análisis por Medidas -->
        {self._generate_medidas_section(metrics['medidas'])}

        <!-- Análisis por Modelos -->
        {self._generate_modelos_section(metrics['modelos'])}

        <!-- Top Productos -->
        <div class="table-container">
            <h3 class="section-title"><i class="fas fa-trophy me-2"></i>Top 50 Productos por Clics</h3>
            <table id="topProductsTable" class="table table-striped table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Producto</th>
                        <th>Marca</th>
                        <th>Categoría</th>
                        <th>Medida</th>
                        <th>Temporada</th>
                        <th>Vehículo</th>
                        <th>Precio</th>
                        <th>Referencia</th>
                        <th>Diff. %</th>
                        <th>Segmento</th>
                        <th>Clics</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_top_products_rows(metrics['top_productos'])}
                </tbody>
            </table>
        </div>

        <!-- Productos de Riesgo -->
        {self._generate_risk_products_section(metrics['productos_riesgo'])}

        <!-- Oportunidades -->
        {self._generate_opportunities_section(metrics['oportunidades'])}

        <!-- Calidad de Datos -->
        <div class="data-quality">
            <h5><i class="fas fa-database me-2"></i>Calidad de Datos</h5>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Total productos CSV:</strong> {metrics['calidad_datos']['total_productos_csv']:,}</p>
                    <p><strong>Total productos feed:</strong> {metrics['calidad_datos']['total_productos_feed']:,}</p>
                    <p><strong>Productos con match:</strong> {metrics['calidad_datos']['productos_con_match']:,}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Productos sin match:</strong> {metrics['calidad_datos']['productos_sin_match']:,}</p>
                    <p><strong>Clics con match:</strong> {metrics['calidad_datos']['clics_con_match']:,}</p>
                    <p><strong>Clics sin match:</strong> {metrics['calidad_datos']['clics_sin_match']:,}</p>
                </div>
            </div>
        </div>

        <!-- Conclusiones y Recomendaciones -->
        <div class="mt-4">
            <h3 class="section-title"><i class="fas fa-chart-pie me-2"></i>Conclusiones y Recomendaciones</h3>

            {self._generate_conclusions(metrics)}
            {self._generate_recommendations(metrics)}
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        // Datos para gráficos
        const chartsData = {json.dumps(charts_data)};

        // Inicializar DataTables
        $(document).ready(function() {{
            $('#brandsTable').DataTable({{
                pageLength: 25,
                order: [[1, 'desc']],
                language: {{
                    url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es.json'
                }}
            }});

            $('#topProductsTable').DataTable({{
                pageLength: 10,
                order: [[7, 'desc']],
                language: {{
                    url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es.json'
                }}
            }});
        }});

        // Gráfico de segmentos
        const segmentCtx = document.getElementById('segmentChart').getContext('2d');
        new Chart(segmentCtx, {{
            type: 'bar',
            data: {{
                labels: chartsData.segments.labels,
                datasets: [{{
                    label: 'Clics por Segmento',
                    data: chartsData.segments.data,
                    backgroundColor: [
                        '#20c997',
                        '#28a745',
                        '#6c757d',
                        '#ffc107',
                        '#dc3545'
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // Gráfico de dispersión
        const scatterCtx = document.getElementById('scatterChart').getContext('2d');
        new Chart(scatterCtx, {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'Productos',
                    data: chartsData.scatter.data,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    pointRadius: 5,
                    pointHoverRadius: 7
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const point = context.raw;
                                return `{{point.title}} - {{point.brand}}: {{point.x}}% diferencia, {{point.y}} clics`;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        title: {{
                            display: true,
                            text: 'Diferencia de Precio (%)'
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: 'Clics'
                        }},
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        return html_content

    def _prepare_charts_data(self, metrics: Dict) -> Dict:
        """Prepara datos para los gráficos Chart.js"""

        # Datos para gráfico de segmentos
        segment_data = metrics['globales']['segmento_distribucion']
        segment_order = ['MUCHO_MAS_BARATO', 'BARATO', 'ALINEADO', 'CARO', 'MUCHO_MAS_CARO']

        segments_labels = []
        segments_data = []
        for segment in segment_order:
            if segment in segment_data:
                segments_labels.append(self._format_segment_label(segment))
                segments_data.append(segment_data[segment])

        # Datos para scatter plot (primeros 100 productos para mejor rendimiento)
        scatter_data = []
        top_products = metrics['top_productos'].head(100)

        for _, product in top_products.iterrows():
            scatter_data.append({
                'x': round(product['price_diff_pct'], 2),
                'y': int(product['Clics']),
                'title': product['Título'][:30] + '...' if len(product['Título']) > 30 else product['Título'],
                'brand': product['Marca']
            })

        return {
            'segments': {
                'labels': segments_labels,
                'data': segments_data
            },
            'scatter': {
                'data': scatter_data
            }
        }

    def _get_position_summary(self, globales: Dict) -> str:
        """Resumen de posición global"""
        segments = globales['segmento_distribucion']

        baratos_pct = segments.get('MUCHO_MAS_BARATO', 0) + segments.get('BARATO', 0)
        caros_pct = segments.get('CARO', 0) + segments.get('MUCHO_MAS_CARO', 0)

        if baratos_pct > caros_pct + 10:
            return "generalmente más baratos"
        elif caros_pct > baratos_pct + 10:
            return "generalmente más caros"
        else:
            return "competitivos"

    def _get_top_brands_summary(self, brands_df: pd.DataFrame) -> str:
        """Resumen de marcas mejor posicionadas"""
        if brands_df is None or len(brands_df) == 0:
            return "No hay datos suficientes"

        top_brands = []
        for _, brand in brands_df.head(3).iterrows():
            if abs(brand['price_diff_media_ponderada']) < 1:
                top_brands.append(brand['marca'])

        if top_brands:
            return f"{', '.join(top_brands)} están bien posicionadas"
        else:
            return f"Principales marcas: {', '.join(brands_df.head(3)['marca'].tolist())}"

    def _get_critical_points_summary(self, metrics: Dict) -> str:
        """Puntos críticos del análisis"""
        risk_count = len(metrics['productos_riesgo'])
        if risk_count > 10:
            return f"Se detectaron {risk_count} productos caros con alto volumen de clics"
        elif risk_count > 0:
            return f"Hay {risk_count} productos que requieren atención inmediata"
        else:
            return "No se detectaron productos críticos"

    def _get_quick_opportunities_summary(self, metrics: Dict) -> str:
        """Oportunidades rápidas"""
        opp_count = len(metrics['oportunidades'])
        if opp_count > 10:
            return f"{opp_count} productos baratos con buen volumen (potencial de subida)"
        elif opp_count > 0:
            return f"{opp_count} productos con oportunidad de optimización"
        else:
            return "Sin oportunidades obvias identificadas"

    def _get_price_class(self, price_diff: float) -> str:
        """Determina clase CSS para diferencia de precio"""
        if price_diff < -1:
            return 'positive'
        elif price_diff > 1:
            return 'negative'
        else:
            return 'neutral'

    def _format_segment_label(self, segment: str) -> str:
        """Formatea etiqueta de segmento"""
        labels = {
            'MUCHO_MAS_BARATO': 'Muy Baratos',
            'BARATO': 'Baratos',
            'ALINEADO': 'Alineados',
            'CARO': 'Caros',
            'MUCHO_MAS_CARO': 'Muy Caros'
        }
        return labels.get(segment, segment)

    def _generate_brands_table_rows(self, brands_df: pd.DataFrame) -> str:
        """Genera filas HTML para tabla de marcas"""
        if brands_df is None or len(brands_df) == 0:
            return '<tr><td colspan="10">No hay datos disponibles</td></tr>'

        rows = []
        for _, brand in brands_df.head(20).iterrows():  # Top 20 marcas
            # Manejar valores nulos con defaults seguros
            marca = brand.get('marca', 'N/A')
            clics_totales = int(brand.get('clics_totales', 0) or 0)
            productos = int(brand.get('productos', 0) or 0)
            price_diff_simple = float(brand.get('price_diff_media_simple', 0) or 0)
            price_diff_ponderada = float(brand.get('price_diff_media_ponderada', 0) or 0)

            segments = brand.get('segmentos') if isinstance(brand.get('segmentos'), dict) else {}

            row = f"""
                <tr>
                    <td><strong>{marca}</strong></td>
                    <td>{clics_totales:,}</td>
                    <td>{productos}</td>
                    <td class="price-{self._get_price_class(price_diff_simple)}">
                        {price_diff_simple:+.2f}%
                    </td>
                    <td class="price-{self._get_price_class(price_diff_ponderada)}">
                        {price_diff_ponderada:+.2f}%
                    </td>
                    <td class="segment-muy-barato">{segments.get('MUCHO_MAS_BARATO', 0):.1f}%</td>
                    <td class="segment-barato">{segments.get('BARATO', 0):.1f}%</td>
                    <td class="segment-alineado">{segments.get('ALINEADO', 0):.1f}%</td>
                    <td class="segment-caro">{segments.get('CARO', 0):.1f}%</td>
                    <td class="segment-muy-caro">{segments.get('MUCHO_MAS_CARO', 0):.1f}%</td>
                </tr>
            """
            rows.append(row)

        return ''.join(rows)

    def _generate_top_products_rows(self, top_products: pd.DataFrame) -> str:
        """Genera filas HTML para tabla de top productos"""
        if top_products is None or len(top_products) == 0:
            return '<tr><td colspan="14">No hay datos disponibles</td></tr>'

        rows = []
        for _, product in top_products.iterrows():
            product_link = product.get('link', '#')

            # Extraer información enriquecida si está disponible
            medida = product.get('medida_final', 'N/A')
            temporada = product.get('temporada_limpia', 'N/A')
            vehiculo = product.get('vehiculo_final', 'N/A')

            # Manejar valores nulos con defaults seguros
            producto_id = product.get('ID de producto', 'N/A')
            titulo = str(product.get('Título', 'N/A'))
            marca = product.get('Marca', 'N/A')

            row = f"""
                <tr>
                    <td>{producto_id}</td>
                    <td title="{titulo}">
                        {titulo[:60]}{'...' if len(titulo) > 60 else ''}
                    </td>
                    <td>{marca}</td>
                    <td>{product.get('category_inferred', 'N/A')}</td>
                    <td>{medida}</td>
                    <td>{temporada}</td>
                    <td>{vehiculo}</td>
                    <td>{float(product.get('Tu precio', 0) or 0):.2f}€</td>
                    <td>{float(product.get('Referencia', 0) or 0):.2f}€</td>
                    <td class="price-{self._get_price_class(float(product.get('price_diff_pct', 0) or 0))}">
                        {float(product.get('price_diff_pct', 0) or 0):+.2f}%
                    </td>
                    <td><span class="badge bg-{self._get_segment_color(product.get('segmento_precio', 'N/A'))}">
                        {product.get('segmento_precio', 'N/A')}
                    </span></td>
                    <td>{int(product.get('Clics', 0) or 0):,}</td>
                    <td><a href="{product_link}" target="_blank" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-external-link-alt"></i>
                    </a></td>
                </tr>
            """
            rows.append(row)

        return ''.join(rows)

    def _generate_temporadas_section(self, temporadas_df: pd.DataFrame) -> str:
        """Genera sección de análisis por temporadas"""
        if temporadas_df is None or len(temporadas_df) == 0:
            return ""

        rows = []
        for _, temporada in temporadas_df.iterrows():
            row = f"""
                <tr>
                    <td><strong>{temporada['temporada']}</strong></td>
                    <td>{temporada['clics_totales']:,}</td>
                    <td>{temporada['productos']}</td>
                    <td class="price-{self._get_price_class(temporada['price_diff_media_ponderada'])}">
                        {temporada['price_diff_media_ponderada']:+.2f}%
                    </td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title"><i class="fas fa-calendar-alt me-2"></i>Análisis por Temporadas</h3>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Temporada</th>
                            <th>Clics Totales</th>
                            <th>Productos</th>
                            <th>Diferencia Precio Ponderada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _generate_vehiculos_section(self, vehiculos_df: pd.DataFrame) -> str:
        """Genera sección de análisis por vehículos"""
        if vehiculos_df is None or len(vehiculos_df) == 0:
            return ""

        rows = []
        for _, vehiculo in vehiculos_df.iterrows():
            row = f"""
                <tr>
                    <td><strong>{vehiculo['vehiculo']}</strong></td>
                    <td>{vehiculo['clics_totales']:,}</td>
                    <td>{vehiculo['productos']}</td>
                    <td class="price-{self._get_price_class(vehiculo['price_diff_media_ponderada'])}">
                        {vehiculo['price_diff_media_ponderada']:+.2f}%
                    </td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title"><i class="fas fa-car me-2"></i>Análisis por Tipo de Vehículo</h3>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Tipo de Vehículo</th>
                            <th>Clics Totales</th>
                            <th>Productos</th>
                            <th>Diferencia Precio Ponderada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _generate_quality_section(self, quality_df: pd.DataFrame) -> str:
        """Genera sección de análisis por segmentos de calidad"""
        if quality_df is None or len(quality_df) == 0:
            return ""

        rows = []
        for _, quality in quality_df.iterrows():
            row = f"""
                <tr>
                    <td><strong>{quality['quality']}</strong></td>
                    <td>{quality['clics_totales']:,}</td>
                    <td>{quality['productos']}</td>
                    <td class="price-{self._get_price_class(quality['price_diff_media_ponderada'])}">
                        {quality['price_diff_media_ponderada']:+.2f}%
                    </td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title"><i class="fas fa-star me-2"></i>Análisis por Segmento de Calidad</h3>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Segmento</th>
                            <th>Clics Totales</th>
                            <th>Productos</th>
                            <th>Diferencia Precio Ponderada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _generate_medidas_section(self, medidas_df: pd.DataFrame) -> str:
        """Genera sección de análisis por medidas"""
        if medidas_df is None or len(medidas_df) == 0:
            return ""

        rows = []
        for _, medida in medidas_df.head(20).iterrows():  # Top 20 medidas
            row = f"""
                <tr>
                    <td><strong>{medida['medida']}</strong></td>
                    <td>{medida['clics_totales']:,}</td>
                    <td>{medida['productos']}</td>
                    <td class="price-{self._get_price_class(medida['price_diff_media_ponderada'])}">
                        {medida['price_diff_media_ponderada']:+.2f}%
                    </td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title"><i class="fas fa-ruler me-2"></i>Top 20 Medidas por Clics</h3>
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>Medida</th>
                            <th>Clics Totales</th>
                            <th>Productos</th>
                            <th>Diferencia Precio Ponderada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _generate_modelos_section(self, modelos_df: pd.DataFrame) -> str:
        """Genera sección de análisis por modelos"""
        if modelos_df is None or len(modelos_df) == 0:
            return ""

        rows = []
        for _, modelo in modelos_df.head(15).iterrows():  # Top 15 modelos
            row = f"""
                <tr>
                    <td><strong>{modelo['modelo']}</strong></td>
                    <td>{modelo['clics_totales']:,}</td>
                    <td>{modelo['productos']}</td>
                    <td class="price-{self._get_price_class(modelo['price_diff_media_ponderada'])}">
                        {modelo['price_diff_media_ponderada']:+.2f}%
                    </td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title"><i class="fas fa-cog me-2"></i>Top 15 Modelos por Clics</h3>
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>Modelo</th>
                            <th>Clics Totales</th>
                            <th>Productos</th>
                            <th>Diferencia Precio Ponderada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _get_segment_color(self, segment: str) -> str:
        """Devuelve color Bootstrap para segmento"""
        colors = {
            'MUCHO_MAS_BARATO': 'success',
            'BARATO': 'success',
            'ALINEADO': 'secondary',
            'CARO': 'warning',
            'MUCHO_MAS_CARO': 'danger'
        }
        return colors.get(segment, 'secondary')

    def _generate_risk_products_section(self, risk_products: pd.DataFrame) -> str:
        """Genera sección de productos de riesgo"""
        if risk_products is None or len(risk_products) == 0:
            return ""

        rows = []
        for _, product in risk_products.head(10).iterrows():
            row = f"""
                <tr>
                    <td>{product['ID de producto']}</td>
                    <td>{product['Título'][:50]}...</td>
                    <td>{product['Marca']}</td>
                    <td class="price-negative">{product['price_diff_pct']:+.2f}%</td>
                    <td>{product['Clics']:,}</td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title text-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>Productos de Riesgo (Caros con muchos clics)
                </h3>
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Producto</th>
                            <th>Marca</th>
                            <th>Diferencia %</th>
                            <th>Clics</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _generate_opportunities_section(self, opportunities: pd.DataFrame) -> str:
        """Genera sección de oportunidades"""
        if opportunities is None or len(opportunities) == 0:
            return ""

        rows = []
        for _, product in opportunities.head(10).iterrows():
            row = f"""
                <tr>
                    <td>{product['ID de producto']}</td>
                    <td>{product['Título'][:50]}...</td>
                    <td>{product['Marca']}</td>
                    <td class="price-positive">{product['price_diff_pct']:+.2f}%</td>
                    <td>{product['Clics']:,}</td>
                </tr>
            """
            rows.append(row)

        return f"""
            <div class="table-container">
                <h3 class="section-title text-success">
                    <i class="fas fa-lightbulb me-2"></i>Oportunidades (Baratos con muchos clics)
                </h3>
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Producto</th>
                            <th>Marca</th>
                            <th>Diferencia %</th>
                            <th>Clics</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

    def _generate_conclusions(self, metrics: Dict) -> str:
        """Genera conclusiones del análisis"""
        segments = metrics['globales']['segmento_distribucion']

        conclusions = []

        # Posición general
        baratos_total = segments.get('MUCHO_MAS_BARATO', 0) + segments.get('BARATO', 0)
        caros_total = segments.get('CARO', 0) + segments.get('MUCHO_MAS_CARO', 0)

        if baratos_total > caros_total + 10:
            conclusions.append("Nuestra estrategia de precios es más agresiva que la competencia, posicionándonos como más baratos en la mayoría de los clics.")
        elif caros_total > baratos_total + 10:
            conclusions.append("Nuestros precios son generalmente más altos que los de la competencia, lo que podría estar impactando negativamente en el volumen de clics.")
        else:
            conclusions.append("Mantenemos una posición competitiva equilibrada, con precios alineados a los del mercado.")

        # Calidad de datos
        match_pct = metrics['calidad_datos']['porcentaje_match']
        if match_pct < 80:
            conclusions.append(f"Se detecta una calidad de datos del {match_pct:.1f}%, recomendable mejorar el mapeo de productos para análisis más precisos.")

        conclusion_html = '<div class="alert alert-info">'
        conclusion_html += '<h5><i class="fas fa-check-circle me-2"></i>Conclusiones Clave</h5>'
        conclusion_html += '<ul>'
        for conclusion in conclusions:
            conclusion_html += f'<li>{conclusion}</li>'
        conclusion_html += '</ul></div>'

        return conclusion_html

    def _generate_recommendations(self, metrics: Dict) -> str:
        """Genera recomendaciones accionables"""
        recommendations = []

        # Análisis de productos de riesgo
        risk_count = len(metrics['productos_riesgo'])
        if risk_count > 0:
            recommendations.append({
                'type': 'critical',
                'title': 'Revisión Inmediata de Precios Altos',
                'description': f'Analizar los {risk_count} productos donde somos más caros y tenemos alto volumen de clics. Considerar ajustes de precios o promociones específicas.'
            })

        # Oportunidades de subida
        opp_count = len(metrics['oportunidades'])
        if opp_count > 5:
            recommendations.append({
                'type': 'opportunity',
                'title': 'Optimización de Márgenes',
                'description': f'Evaluar posibilidad de aumentar precios en {opp_count} productos donde estamos significativamente más baratos sin afectar el volumen.'
            })

        # Análisis por marca
        if metrics['marcas'] is not None and len(metrics['marcas']) > 0:
            problematic_brands = metrics['marcas'][
                metrics['marcas']['price_diff_media_ponderada'] > 2
            ].head(3)

            if len(problematic_brands) > 0:
                brands_list = ', '.join(problematic_brands['marca'].tolist())
                recommendations.append({
                    'type': 'warning',
                    'title': 'Ajuste por Marca',
                    'description': f'Revisar estrategia de precios para marcas: {brands_list}, donde superamos consistentemente los precios de referencia.'
                })

        # Recomendación general
        recommendations.append({
            'type': 'general',
            'title': 'Monitoreo Continuo',
            'description': 'Establecer alertas automáticas para productos que desvíen su posición competitiva más del ±5% mensualmente.'
        })

        rec_html = '<h5><i class="fas fa-tasks me-2"></i>Recomendaciones Accionables</h5>'
        for rec in recommendations:
            icon_map = {
                'critical': 'fas fa-exclamation-triangle text-danger',
                'opportunity': 'fas fa-coins text-success',
                'warning': 'fas fa-exclamation-circle text-warning',
                'general': 'fas fa-chart-line text-info'
            }

            rec_html += f"""
                <div class="recommendation mb-3">
                    <h6><i class="{icon_map.get(rec['type'], 'fas fa-info-circle')} me-2"></i>{rec['title']}</h6>
                    <p class="mb-0">{rec['description']}</p>
                </div>
            """

        return rec_html