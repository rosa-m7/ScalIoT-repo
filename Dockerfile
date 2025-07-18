FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app


# Copiar requirements primero (para mejor cache de Docker)
COPY requirements.txt .

# Actualizar pip e instalar dependencias
RUN pip3 install --upgrade pip
RUN pip3 cache purge
RUN pip3 install -r requirements.txt --no-cache-dir

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando corregido para ejecutar Flask
CMD ["python", "-m", "flask", "--app", "my-app.run", "run", "--host=0.0.0.0", "--port=8080"]