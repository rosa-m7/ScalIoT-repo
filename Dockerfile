FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]