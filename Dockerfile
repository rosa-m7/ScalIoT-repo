FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip y herramientas de instalación
RUN pip install --upgrade pip setuptools wheel

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para mejor cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Verificar instalación
RUN pip check

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar Flask
CMD ["python", "-m", "flask", "--app", "my-app.run", "run", "--host=0.0.0.0", "--port=8080"]
