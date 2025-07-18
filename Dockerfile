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

# Actualizar pip PRIMERO
RUN pip install --upgrade pip

# Copiar requirements primero (para mejor cache de Docker)
COPY requirements.txt .

# SOLUCIÓN AL CONFLICTO DE PYTZ:
# 1. Instalar pytz==2025.2 específicamente primero
RUN pip install --no-cache-dir pytz==2025.2

# 2. Instalar el resto sin pytz para evitar conflictos
RUN grep -v "pytz" requirements.txt > requirements_temp.txt
RUN pip install --no-cache-dir -r requirements_temp.txt

# 3. Limpiar archivo temporal
RUN rm requirements_temp.txt

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando corregido para ejecutar Flask
CMD ["python", "-m", "flask", "--app", "my-app.run", "run", "--host=0.0.0.0", "--port=8080"]