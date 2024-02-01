# Usa una imagen base de Python 3 con Debian Buster
FROM python:3.9-slim-buster

# Evita preguntas interactivas al utilizar apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Actualiza el índice de paquetes e instala las dependencias necesarias para la compilación
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    gcc \
    libc6-dev \
    python3-dev \
    linux-headers-amd64 \
    make \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app
RUN mkdir -p /app/logs

# Instala las dependencias de Python desde el archivo requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta tu script
CMD ["python", "./app.py"]