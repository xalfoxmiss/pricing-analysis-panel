# 📊 Panel Analizador de Precios - Guía de Deployment

## 🚀 Opciones de Deployment (GRATIS)

### 1. Streamlit Cloud (Más fácil - recomendado para MVP)

**Paso 1: Preparar el repositorio**
```bash
# Instalar Streamlit
pip install streamlit

# Probar localmente
streamlit run app.py
```

**Paso 2: Subir a GitHub**
```bash
git init
git add .
git commit -m "Panel analizador de precios v1.0"
git branch -M main
git remote add origin https://github.com/tu-usuario/analizador-precios.git
git push -u origin main
```

**Paso 3: Deploy en Streamlit Cloud**
1. Ir a [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Crear cuenta gratuita
3. Conectar tu repositorio de GitHub
4. Seleccionar el archivo `app.py` como punto de entrada
5. ¡Listo! Tu app estará en: https://tu-app.share.streamlit.io

---

### 2. Railway.app (Opción alternativa)

```bash
# Crear archivo railway.json
echo '{ "build": { "builder": "NIXPACKS" }, "deploy": { "startCommand": "streamlit run app.py --server.port=$PORT", "restartPolicyType": "ON_FAILURE" } }' > railway.json

# Comandos de deploy
git add .
git commit -m "Add railway.json"
git push
```

Luego en Railway.app:
1. Conectar tu repositorio GitHub
2. Railway detectará automáticamente el proyecto
3. Deploy automático en: https://tu-app.railway.app

---

### 3. Render.com (Opción alternativa)

**Crear `render.yaml`:**
```yaml
services:
  type: web
  name: analizador-precios
  env: python
  plan: free
  buildCommand: pip install -r requirements.txt
  startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  healthCheckPath: /
```

---

## 📋 Archivos del Proyecto

```
merchant-precios/
├── app.py                          # Panel principal (Streamlit)
├── pricing_analyzer.py             # Motor de análisis de datos
├── report_generator.py             # Generador de informes HTML
├── requirements.txt                 # Dependencias Python
├── README_DEPLOYMENT.md            # Esta guía
├── precios.csv                     # Archivo CSV de ejemplo
└── feed.xml                        # Archivo XML de ejemplo
```

---

## 🔧 Requisitos del Sistema

### Dependencias (requirements.txt)
```
streamlit==1.29.0
pandas==2.1.4
numpy==1.26.2
lxml==5.0.0
plotly==5.18.0
python-dateutil==2.8.2
```

### Sistema Operativo
- ✅ Windows 10/11
- ✅ macOS
- ✅ Linux (Ubuntu, Debian)

### Python
- ✅ Python 3.8+
- Recomendado: Python 3.9 o 3.10

---

## 🚀 Ejecución Local

### Opción 1: Directo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar panel
streamlit run app.py
```

### Opción 2: Entorno virtual (recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

El panel estará disponible en: http://localhost:8501

---

## 📊 Uso del Panel

### 1. Subir Archivos
- **Archivo A**: CSV de competitividad de Google Merchant Center
- **Archivo B**: XML de feed de productos

### 2. Procesamiento
- Click en "GENERAR INFORME"
- El sistema procesa automáticamente los datos

### 3. Resultados
- KPIs principales en tiempo real
- Métricas detalladas por categoría
- Descarga del informe HTML completo

---

## 🔧 Personalización

### Cambiar colores/títulos
Editar las clases CSS en `app.py`:
```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        /* ... */
    }
</style>
""", unsafe_allow_html=True)
```

### Agregar nuevas métricas
Modificar `pricing_analyzer.py` en la función `calculate_metrics()`.

### Modificar informe HTML
Editar `report_generator.py` para personalizar el informe de salida.

---

## 🛠️ Troubleshooting

### Error: "File not found"
- Verifica que los archivos estén en el formato correcto
- El CSV debe tener la estructura de Google Merchant Center

### Error: "Memory limit exceeded"
- Para datasets muy grandes, considera optimizar el procesamiento
- Puedes limitar el número de productos procesados

### Error: "Package not found"
- Ejecuta: `pip install -r requirements.txt`
- Verifica la versión de Python (>= 3.8)

---

## 💡 Tips Pro

### Para mejor rendimiento
1. **Limitar datasets**: Agrega límites para archivos muy grandes
2. **Caching**: Implementa caché para análisis repetidos
3. **Lazy loading**: Carga datos solo cuando sea necesario

### Para mejor UX
1. **Barra de progreso**: Agrega indicadores de progreso para procesos largos
2. **Validación**: Valida archivos antes del procesamiento
3. **Errores amigables**: Mensajes de error claros y con soluciones

### Para scalability
1. **Database**: Integra PostgreSQL para almacenar históricos
2. **APIs**: Conecta con APIs externas para datos en tiempo real
3. **Scheduler**: Agrega programación de análisis automáticos

---

## 📈 Mejoras Futuras

### MVP Actual
- ✅ Upload de archivos CSV/XML
- ✅ Análisis automático
- ✅ Informe HTML interactivo
- ✅ Descarga de resultados

### Versión Pro
- 🔄 Programación automática
- 📊 Dashboard con gráficos Plotly
- 🔐 Autenticación de usuarios
- 💾 Base de datos históricos
- 📧 Notificaciones por email
- 🔌 Integración APIs externas

---

## 🆘 Soporte

### Documentación oficial
- [Streamlit Docs](https://docs.streamlit.io/)
- [Pandas Docs](https://pandas.pydata.org/)
- [Plotly Docs](https://plotly.com/python/)

### Comunidad
- [Streamlit Community](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

## 📝 Licencia

Este proyecto es de código abierto. Siéntete libre de:
- ✅ Usar para proyectos comerciales
- ✅ Modificar y adaptar
- ✅ Contribuir con mejoras
- 📄 Atribución apreciada (no requerida)

---

**¡Listo para deploy! 🚀**