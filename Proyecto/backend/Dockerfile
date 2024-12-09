FROM python:3.11-slim as build-stage

# Instalar dependencias necesarias para Node.js
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos de Python
COPY requirements.txt ./

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias de Node.js (si tienes package.json en tu proyecto)
COPY package*.json ./
RUN npm install

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto para FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
