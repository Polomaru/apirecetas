FROM python:3-slim

# Instalamos las dependencias del sistema necesarias para mysqlclient
RUN apt-get update && \
    apt-get install -y \
    gcc \
    libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /programas/apirecetas

# Instalamos las dependencias de Python
RUN pip3 install flask flask-mysqldb

# Copia los archivos de tu aplicación al contenedor
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la app en puerto 8000
CMD ["python3", "app.py"]
