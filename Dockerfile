FROM python:3.9-slim

WORKDIR /app

# Copiar requirements primero para aprovechar caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]