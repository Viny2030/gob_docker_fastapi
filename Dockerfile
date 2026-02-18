FROM python:3.11-slim
WORKDIR /app

# Instalamos dependencias del sistema para Excel
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copiamos y cargamos librerías [cite: 1]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Aseguramos la ruta de datos que solicitaste
RUN mkdir -p /app/gob_docker/data

EXPOSE 8501

# Ejecución corregida apuntando a main.py
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableStaticServing=true"]