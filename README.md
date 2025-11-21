# 📊 Pricing Analysis Panel

Panel web automatizado para análisis de competitividad de precios a partir de datos de Google Merchant Center con análisis multi-dimensional avanzado.

## 🚀 Características Principales

### 📈 **Análisis Multi-Dimensional**
- **Marcas**: Análisis de competitividad por fabricante
- **Categorías**: Desglose por categorías de productos del feed
- **Atributos**: Análisis por atributos específicos de `g:product_detail`
- **Labels**: Segmentación por `g:custom_label_0-4`
- **Temporadas**: Productos por temporadas o estacionalidad
- **Calidad**: Segmentos por calidad o categorías personalizadas

### 🔧 **Características Técnicas**
- **Parser XML Avanzado**: Compatible con feeds Google Shopping con namespace `g:*`
- **Panel Web Interactivo**: Interfaz Streamlit con upload drag & drop
- **Informes HTML Profesionales**: Reportes automáticos con KPIs, gráficos y tablas interactivas
- **Docker Ready**: Contenedores para deployment fácil
- **Multi-plataforma**: Compatible con Google Merchant Center de cualquier sector

## 🛠️ Stack Tecnológico

- **Streamlit 1.40.0** - Framework web para paneles interactivos
- **Pandas 2.2.3** - Análisis y manipulación de datos
- **Plotly 5.24.1** - Visualizaciones interactivas
- **lxml 5.3.0** - Parser de XML con soporte de namespaces
- **Bootstrap 5** - UI responsiva y componentes modernos
- **Python 3.8+** - Lenguaje principal (compatible hasta Python 3.13+)

## 📋 Requisitos

- Python 3.8 o superior
- 2GB RAM mínimo (recomendado 4GB+ para datasets grandes)
- Espacio en disco para archivos CSV/XML

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución Directa
```bash
# Clonar repositorio
git clone https://github.com/xalfoxmiss/pricing-analysis-panel.git
cd pricing-analysis-panel

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar panel
streamlit run app.py
```

### Opción 2: Entorno Virtual (Recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar panel
streamlit run app.py
```

### Opción 3: Script Automatizado
```bash
# Script con verificación automática de dependencias
python run_panel.py
```

El panel estará disponible en http://localhost:8501

## 🐳 Docker

### Construcción y Ejecución
```bash
# Construir imagen
docker build -t pricing-analysis-panel .

# Ejecutar contenedor
docker run -p 8501:8501 pricing-analysis-panel
```

### Docker Compose
```bash
docker-compose up
```

## 📊 Uso del Panel

### 1. Subida de Archivos
- **Archivo A**: CSV de competitividad de Google Merchant Center
  - Columnas requeridas: `SKU`, `Clics`, `Impresiones`, `Precio`
  - Formato: UTF-8, separador coma
- **Archivo B**: XML feed de productos Google Shopping
  - Namespace: `http://base.google.com/ns/1.0`
  - Campos soportados: `g:price`, `g:brand`, `g:product_detail`

### 2. Procesamiento Automático
- Click en **"GENERAR INFORME"**
- Análisis automático de datos
- Procesamiento de XML con extracción de atributos

### 3. Resultados
- **KPIs Principales**: Métricas clave en tiempo real
- **Análisis por Dimensiones**: Desglose detallado por cada categoría
- **Top Products**: Productos mejor/peor posicionados
- **Descarga de Informe**: Reporte HTML completo con gráficos interactivos

## 📁 Estructura del Proyecto

```
pricing-analysis-panel/
├── app.py                    # Panel principal Streamlit (400+ líneas)
├── pricing_analyzer.py       # Motor de análisis de datos (500+ líneas)
├── report_generator.py       # Generador de informes HTML (600+ líneas)
├── requirements.txt          # Dependencias Python
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Orquestación Docker
├── run_panel.py            # Script de ejecución local
├── reports/                # Carpeta de informes generados (gitignore)
├── .gitignore              # Archivos excluidos del repo
└── README.md               # Este archivo
```

## 🎯 Análisis Detallado

### Extracción de Datos XML
El parser extrae automáticamente:
- **Campos estándar**: `g:id`, `g:title`, `g:price`, `g:brand`
- **Detalles de producto**: `g:product_detail` con sección y atributo personalizado
- **Labels personalizados**: `g:custom_label_0-4` para segmentos personalizados
- **Dimensiones**: `g:dimensions`, `g:pattern` para categorías específicas

### Métricas Calculadas
- **Diferencia de precio**: Porcentaje vs competencia
- **Segmentos de competitividad**: MUCHO_MAS_BARATO, BARATO, ALINEADO, CARO, MUCHO_MAS_CARO
- **KPIs de rendimiento**: Clics, impresiones, CTR por segmento
- **Oportunidades**: Productos con potencial de mejora

### Reportes Generados
- **Resumen Ejecutivo**: KPIs principales y tendencias
- **Análisis por Marca**: Competitividad por fabricante
- **Análisis por Categorías**: Desglose por categorías del feed y atributos
- **Análisis por Labels**: Segmentación por custom_labels
- **Top Products**: Ranking de productos por rendimiento
- **Recomendaciones**: Acciones sugeridas por prioridad

## 🌐 Deployment

### Opciones Gratuitas

#### 1. Streamlit Cloud (Recomendado)
1. Ir a [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Crear cuenta gratuita
3. Conectar repositorio GitHub: `xalfoxmiss/pricing-analysis-panel`
4. Seleccionar `app.py` como punto de entrada
5. URL resultante: `https://xalfoxmiss-pricing-analysis-panel.streamlit.app`

#### 2. Railway.app
```bash
# Crear railway.json
echo '{
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
    "restartPolicyType": "ON_FAILURE"
  }
}' > railway.json

git add railway.json
git commit -m "Add Railway config"
git push
```

#### 3. Render.com
```yaml
# render.yaml
services:
  type: web
  name: pricing-analysis-panel
  env: python
  plan: free
  buildCommand: pip install -r requirements.txt
  startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  healthCheckPath: /
```

### Requisitos de Sistema para Deployment

- **Python**: 3.8+ (recomendado 3.9-3.10)
- **Memoria**: Mínimo 1GB, recomendado 2GB+
- **Storage**: 500MB+ para dependencias y datos
- **Red**: Conexión a internet para feeds XML

## 🔧 Personalización y Configuración

### Modificar Estilos
Editar CSS en `app.py` (líneas 27-88):
```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    /* ... más estilos ... */
</style>
""", unsafe_allow_html=True)
```

### Agregar Nuevas Métricas
Modificar `pricing_analyzer.py` en función `calculate_metrics()`:
```python
def calculate_metrics(self):
    # Métricas existentes...

    # Agregar nueva métrica
    df['nueva_metrica'] = tu_calculo

    return {
        'metrics_globales': global_metrics,
        'brand_analysis': brand_metrics,
        'nueva_metrica': df['nueva_metrica'].describe()
    }
```

### Personalizar Informes HTML
Editar plantillas en `report_generator.py`:
```python
def generate_report(self, metrics, data):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Informe Personalizado</title>
        <!-- Estilos personalizados -->
    </head>
    <body>
        <!-- Tu contenido personalizado -->
    </body>
    </html>
    """
    return html_template
```

## 🛠️ Troubleshooting

### Errores Comunes

#### "File not found"
- **Solución**: Verificar formatos CSV/XML y permisos de archivos
- **CSV debe tener**: Headers correctos, formato UTF-8
- **XML debe tener**: Namespace `http://base.google.com/ns/1.0`

#### "Memory limit exceeded"
- **Solución**: Optimizar para datasets grandes
```python
# Limitar número de productos
if len(df) > 10000:
    df = df.head(10000)
```

#### "Package not found"
- **Solución**: Instalar dependencias correctas
```bash
pip install -r requirements.txt
python --version  # Verificar >= 3.8
```

#### "XML parsing error"
- **Solución**: Validar namespace y estructura XML
```xml
<!-- Verificar namespace correcto -->
<rss xmlns:g="http://base.google.com/ns/1.0">
```

### Optimización de Rendimiento

#### Para Datasets Grandes
1. **Limitar procesamiento**: Máximo 10,000 productos
2. **Caching**: Guardar resultados intermedios
3. **Lazy loading**: Cargar datos solo cuando sea necesario

#### Para Mejor UX
1. **Barras de progreso**: Indicadores visuales
2. **Validación previa**: Verificar archivos antes de procesar
3. **Mensajes claros**: Errores amigables con soluciones

## 💡 Tips Pro

### Desarrollo
- **Entorno virtual**: Siempre usar venv para desarrollo
- **Testing**: Probar con datasets pequeños primero
- **Logging**: Agregar logs para debugging
- **Version control**: Commits frecuentes con mensajes claros

### Deployment
- **Ambientes**: Separar desarrollo/producción
- **Monitorización**: Métricas de uso y performance
- **Backups**: Copias de seguridad de datos importantes
- **Updates**: Actualizar dependencias regularmente

### Seguridad
- **Validación**: Sanitizar inputs de usuario
- **Permisos**: Acceso restringido a datos sensibles
- **HTTPS**: Usar siempre en producción
- **Secrets**: Nunca commitear credenciales

## 📈 Roadmap y Mejoras Futuras

### Versión 2.0 (Planeado)
- 🔄 **Programación automática**: Análisis periódicos
- 📊 **Gráficos Plotly**: Visualizaciones avanzadas
- 🔐 **Autenticación**: Usuarios y roles
- 💾 **Base de datos**: PostgreSQL para históricos
- 📧 **Notificaciones**: Email de alertas
- 🔌 **APIs**: Integración con servicios externos

### Versión 3.0 (Futuro)
- 🤖 **Machine Learning**: Predicción de precios
- 📱 **Mobile app**: Versión móvil
- 🌍 **Multi-idioma**: Soporte internacional
- 🔄 **Real-time**: Actualizaciones en vivo
- ☁️ **Cloud-native**: Arquitectura escalable

## 🆘 Soporte y Comunidad

### Documentación Oficial
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [Google Merchant Center Help](https://support.google.com/merchants/)

### Comunidad
- [Streamlit Community](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/xalfoxmiss/pricing-analysis-panel/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/streamlit)

### Reportar Issues
Para reportar bugs o solicitar features:
1. Crear issue en [GitHub](https://github.com/xalfoxmiss/pricing-analysis-panel/issues)
2. Incluir: Sistema operativo, versión Python, dataset de ejemplo
3. Describir pasos para reproducir el problema

## 📝 Licencia

Este proyecto es de código abierto bajo licencia MIT.

✅ **Permitido**:
- Uso comercial
- Modificación y adaptación
- Distribución
- Uso privado

📄 **Atribución**: Agradecida pero no requerida

## 👨‍💻 Autor

**[Alfonso Calero](https://www.alfonsocalero.es/)**

- 🔗 **Website**: https://www.alfonsocalero.es/
- 📧 **Email**: Disponible en web
- 🐙 **GitHub**: @xalfoxmiss
- 💼 **LinkedIn**: [Perfil](https://www.linkedin.com/in/alfonsocalerogijon/)

---

## 🚀 Quick Start

```bash
# Clone y setup en un comando
git clone https://github.com/xalfoxmiss/pricing-analysis-panel.git && \
cd pricing-analysis-panel && \
pip install -r requirements.txt && \
streamlit run app.py
```

**¡Listo para usar en http://localhost:8501! 🎉**

---

*Última actualización: 21 noviembre de 2025*