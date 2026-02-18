# Dockerfile para Railway
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/gob_docker/data

# EXPOSE es informativo, Railway usa el puerto dinámico
EXPOSE 8501

# CAMBIO CLAVE: Usamos el puerto que Railway nos asigne mediante la variable de entorno PORT
CMD ["sh", "-c", "streamlit run main.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.enableStaticServing=true"]