from flask import Flask, request, jsonify
from flasgger import Swagger
import mysql.connector
from datetime import datetime
import pytz

zona_local = pytz.timezone('America/Lima')  # Cambia a tu zona
hoy = datetime.now(zona_local).strftime('%Y-%m-%d')
import uuid

app = Flask(__name__)
swagger = Swagger(app)

# Configuración de la base de datos
db_config = {
    'host': '172.31.24.145',
    'port': 8005,
    'user': 'root',
    'password': 'utec',
    'database': 'citasdb'
}

def get_db_connection():
    return mysql.connector.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

### --- CITAS --- ###

@app.route('/generarcita', methods=['POST'])
def crear_cita():
    """
    Crear una nueva cita médica
    ---
    tags:
      - Citas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - idpaciente
            - iddoctor
            - especialidad
            - fecha_hora
            - tipo
          properties:
            idcita:
              type: string
            idpaciente:
              type: string
            iddoctor:
              type: string
            especialidad:
              type: string
            fecha_hora:
              type: string
              format: date-time
            tipo:
              type: string
    responses:
      201:
        description: Cita creada correctamente
      400:
        description: Faltan campos obligatorios
      500:
        description: Error del servidor
    """
    data = request.get_json()
    campos = ['idpaciente', 'iddoctor', 'especialidad', 'fecha_hora', 'tipo']
    if not all(c in data for c in campos):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    idcita = str(uuid.uuid4())

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO citas (idcita, idpaciente, iddoctor, especialidad, fecha_hora, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            idcita,
            data['idpaciente'],
            data['iddoctor'],
            data['especialidad'],
            data['fecha_hora'],
            data['tipo']
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Cita creada correctamente', 'idcita': idcita}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getcita/<idcita>', methods=['GET'])
def obtener_cita(idcita):
    """
    Obtener una cita por ID
    ---
    tags:
      - Citas
    parameters:
      - name: idcita
        in: path
        type: string
        required: true
    responses:
      200:
        description: Cita encontrada
      400:
        description: Cita no encontrada
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE idcita = %s", (idcita,))
    cita = cursor.fetchone()
    cursor.close()
    connection.close()
    if not cita:
        return jsonify({'message': 'Cita no encontrada', 'data': None}), 400 
    return jsonify({'message': 'Cita encontrada', 'data': cita}), 200


@app.route('/getcita/paciente/<idpaciente>', methods=['GET'])
def obtener_citas_por_paciente(idpaciente):
    """
    Obtener todas las citas de un paciente
    ---
    tags:
      - Citas
    parameters:
      - name: idpaciente
        in: path
        type: string
        required: true
    responses:
      200:
        description: Lista de citas del paciente
      400:
        description: No se encontraron citas para el paciente
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE idpaciente = %s ORDER BY fecha_hora DESC", (idpaciente,))
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not citas:
        return jsonify({'message': 'No se encontraron citas para este paciente', 'data': []}), 400  
    return jsonify({'message': 'Citas encontradas', 'data': citas}), 200


@app.route('/getcitas/doctor/<iddoctor>', methods=['GET'])
def obtener_citas_por_doctor(iddoctor):
    """
    Obtener todas las citas de un doctor
    ---
    tags:
      - Citas
    parameters:
      - name: iddoctor
        in: path
        type: string
        required: true
    responses:
      200:
        description: Lista de citas del doctor
      400:
        description: No se encontraron citas para el doctor
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE iddoctor = %s ORDER BY fecha_hora DESC", (iddoctor,))
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not citas:
        return jsonify({'message': 'No se encontraron citas para este doctor', 'data': []}), 400 
    return jsonify({'message': 'Citas encontradas', 'data': citas}), 200


@app.route('/getcita/hoy', methods=['GET'])
def obtener_citas_hoy():
    """
    Obtener citas para el día de hoy
    ---
    tags:
      - Citas
    responses:
      200:
        description: Lista de citas para hoy
      400:
        description: No hay citas programadas para hoy
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE DATE(fecha_hora) = %s", (hoy,))
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not citas:
        return jsonify({'message': 'No hay citas programadas para hoy', 'data': []}), 400
    return jsonify({'message': 'Citas para hoy encontradas', 'data': citas}), 200


### --- RECETAS --- ###

 # Asegúrate de tener esta importación

@app.route('/generarreceta', methods=['POST'])
def generar_receta():
    """
    Generar una nueva receta médica
    ---
    tags:
      - Recetas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - idcita
            - medicamentos
            - idpaciente
            - iddoctor
            - diagnostico
            - requiere_examen_medico
          properties:
            idcita:
              type: string
            medicamentos:
              type: string
            idpaciente:
              type: string
            iddoctor:
              type: string
            diagnostico:
              type: string
            requiere_examen_medico:
              type: boolean
            duracion:
              type: string
            observaciones:
              type: string
    responses:
      201:
        description: Receta creada correctamente
      400:
        description: Faltan campos obligatorios
      500:
        description: Error del servidor
    """
    data = request.get_json()
    campos = ['idcita', 'medicamentos', 'idpaciente', 'iddoctor', 'diagnostico', 'requiere_examen_medico']
    if not all(c in data for c in campos):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    idreceta = str(uuid.uuid4())
    fecha_emision = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Usamos la fecha actual

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO recetas (
                idreceta, idcita, fecha_emision, medicamentos,
                idpaciente, iddoctor, diagnostico, duracion,
                observaciones, requiere_examen_medico
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            idreceta,
            data['idcita'],
            fecha_emision,
            data['medicamentos'],
            data['idpaciente'],
            data['iddoctor'],
            data['diagnostico'],
            data.get('duracion'),
            data.get('observaciones'),
            data['requiere_examen_medico']
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Receta creada correctamente', 'idreceta': idreceta}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getrecetas/paciente/<idpaciente>', methods=['GET'])
def obtener_recetas_por_paciente(idpaciente):
    """
    Obtener recetas por ID de paciente
    ---
    tags:
      - Recetas
    parameters:
      - name: idpaciente
        in: path
        type: string
        required: true
    responses:
      200:
        description: Lista de recetas
      400:
        description: No se encontraron recetas para este paciente
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recetas WHERE idpaciente = %s ORDER BY fecha_emision DESC", (idpaciente,))
    recetas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not recetas:
        return jsonify({'message': 'No se encontraron recetas para este paciente', 'data': []}), 400
    return jsonify({'message': 'Recetas encontradas', 'data': recetas}), 200


@app.route('/getrecetas/doctor/<iddoctor>', methods=['GET'])
def obtener_recetas_por_doctor(iddoctor):
    """
    Obtener recetas por ID de doctor
    ---
    tags:
      - Recetas
    parameters:
      - name: iddoctor
        in: path
        type: string
        required: true
    responses:
      200:
        description: Lista de recetas
      400:
        description: No se encontraron recetas para este doctor
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recetas WHERE iddoctor = %s ORDER BY fecha_emision DESC", (iddoctor,))
    recetas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not recetas:
        return jsonify({'message': 'No se encontraron recetas para este doctor', 'data': []}), 400
    return jsonify({'message': 'Recetas encontradas', 'data': recetas}), 200

@app.route('/getreceta/cita/<idcita>', methods=['GET'])
def obtener_receta_por_cita(idcita):
    """
    Obtener receta por ID de cita
    ---
    tags:
      - Recetas
    parameters:
      - name: idcita
        in: path
        type: string
        required: true
    responses:
      200:
        description: Receta encontrada
      400:
        description: No se encontró receta para esta cita
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recetas WHERE idcita = %s", (idcita,))
    receta = cursor.fetchone()
    cursor.close()
    connection.close()
    if not receta:
        return jsonify({'message': 'No se encontró receta para esta cita', 'data': None}), 400
    return jsonify({'message': 'Receta encontrada', 'data': receta}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
