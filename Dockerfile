FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Para MySQL
    default-libmysqlclient-dev \
    # Compiladores
    gcc \
    g++ \
    # Para cryptography y Firebase
    libffi-dev \
    libssl-dev \
    pkg-config \
    # Para Matplotlib y librerías científicas
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip y herramientas de instalación
RUN pip install --upgrade pip setuptools wheel

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para mejor cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip check

# Copiar todo el código
COPY . .

EXPOSE 8080

CMD ["python", "-m", "flask", "--app", "my-app/run", "run", "--host=0.0.0.0", "--port=8080"]