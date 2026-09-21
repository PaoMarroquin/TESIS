# Imagen base liviana con Python
FROM python:3.12-slim

# Evita que Python guarde archivos .pyc y que bufferee los logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para compilar psycopg / pgvector
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Se copia primero solo requirements.txt para aprovechar la cache de Docker:
# si no cambias dependencias, no se reinstalan en cada build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora sí se copia el resto del código
COPY . .

EXPOSE 8000

# --reload solo sirve en desarrollo (ver docker-compose.yml).
# En producción (Render) se usa este mismo Dockerfile pero sin --reload.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
