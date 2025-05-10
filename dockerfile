FROM python:3-slim

# Establecer el directorio de trabajo
WORKDIR /programas/apirecetas

# Instalar las dependencias necesarias en un solo RUN
RUN pip3 install flask mysql-connector-python

# Copiar los archivos de la aplicación
COPY . .

# Comando para ejecutar la aplicación Flask
CMD ["python3", "app.py", "--port", "8000"]
