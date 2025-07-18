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

# Actualizar pip e instalar pip-tools
RUN pip install --upgrade pip
RUN pip install pip-tools

# Generar requirements resueltos
RUN pip-compile --resolver=backtracking --allow-unsafe requirements.txt

# Instalar dependencias con resolución forzada
RUN pip install --no-cache-dir -r requirements.txt --force-reinstall

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar Flask
CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8080"]