FROM python:3-slim

WORKDIR /programas/api-clinica

# Instalación de dependencias necesarias
RUN pip3 install flask flask-mysqldb

# Copia los archivos de tu aplicación al contenedor
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la app en puerto 8000
CMD ["python3", "app.py"]
