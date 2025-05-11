
# 🏥 Microservicio de Consultas y Recetas Médicas

Este proyecto forma parte de un sistema de microservicios diseñado para la gestión de una clínica médica. En particular, este microservicio se encarga de la gestión de consultas y recetas médicas, permitiendo almacenar, consultar y administrar información relacionada con las atenciones médicas y las prescripciones realizadas a los pacientes.

## 🚀 Características

* 📄 **Gestión de consultas y recetas**: Permite crear, leer, actualizar y eliminar registros de consultas médicas y sus respectivas recetas.
* 🗄️ **Persistencia de datos**: Utiliza una base de datos relacional para almacenar la información de manera estructurada y segura.
* 🐳 **Contenerización**: Incluye un `Dockerfile` para facilitar la implementación y despliegue del microservicio en entornos controlados.

## 🛠️ Tecnologías utilizadas

* **Python**: Lenguaje de programación principal utilizado en el desarrollo del microservicio.
* **Flask**: Framework web ligero para la creación de APIs RESTful.
* **MySQL** : Sistema de gestión de bases de datos relacional.
* **Docker**: Plataforma para contenerizar aplicaciones y facilitar su despliegue.

## 📁 Estructura del proyecto



````
apirecetas/
├── app.py          # Archivo principal de la aplicación
├── base.sql        # Script de creación de la base de datos
└── dockerfile      # Archivo de configuración para Docker
````

## ⚙️ Instalación y ejecución

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/Polomaru/apirecetas.git
   cd apirecetas
   ```

2. **Construir y ejecutar el contenedor Docker**:

   ```bash
   docker build -t apirecetas .
   docker run -p 8000:8000 apirecetas
   ```

   La API estará disponible en `http://MV:8000`.

## 📬 Endpoints disponibles

### Consultas

* **GET** `/getcita/<idcita>`: Obtiene una cita por ID de cita.

  * **Parámetros**: `idcita` (string, requerido)
  * **Respuestas**:

    * `200 OK`: Cita encontrada.
    * `400 Bad Request`: Cita no encontrada.

* **GET** `/getcita/paciente/<idpaciente>`: Obtiene todas las citas de un paciente.

  * **Parámetros**: `idpaciente` (string, requerido)
  * **Respuestas**:

    * `200 OK`: Lista de citas encontradas o mensaje indicando que no hay citas para este paciente.
    * `400 Bad Request`: Si no se encuentra ninguna cita para el paciente.

* **GET** `/getcitas/doctor/<iddoctor>`: Obtiene todas las citas de un doctor.

  * **Parámetros**: `iddoctor` (string, requerido)
  * **Respuestas**:

    * `200 OK`: Lista de citas encontradas o mensaje indicando que no hay citas para este doctor.
    * `400 Bad Request`: Si no se encuentran citas para el doctor.

* **GET** `/getcita/hoy`: Obtiene las citas para el día de hoy.

  * **Respuestas**:

    * `200 OK`: Lista de citas encontradas para hoy.
    * `400 Bad Request`: Si no hay citas programadas para hoy.

### Recetas

* **GET** `/getrecetas/paciente/<idpaciente>`: Obtiene todas las recetas de un paciente.

  * **Parámetros**: `idpaciente` (string, requerido)
  * **Respuestas**:

    * `200 OK`: Lista de recetas encontradas.
    * `400 Bad Request`: Si no se encuentran recetas para el paciente.

* **GET** `/getrecetas/doctor/<iddoctor>`: Obtiene todas las recetas de un doctor.

  * **Parámetros**: `iddoctor` (string, requerido)
  * **Respuestas**:

    * `200 OK`: Lista de recetas encontradas.
    * `400 Bad Request`: Si no se encuentran recetas para el doctor.

* **GET** `/getreceta/cita/<idcita>`: Obtiene la receta asociada a una cita.

  * **Parámetros**: `idcita` (string, requerido)
  * **Respuestas**:

    * `200 OK`: Receta encontrada.
    * `400 Bad Request`: Si no hay receta asociada a la cita.
