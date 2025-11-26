FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (más completas para tus librerías)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Para MySQL
    default-libmysqlclient-dev \
    # Compiladores
    gcc \
    g++ \
    # Para Matplotlib y librerías científicas
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    # Para cryptography
    libssl-dev \
    libffi-dev \
    # Para gRPC (Firebase)
    pkg-config \
    # Limpiar cache
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]