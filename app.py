from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import uuid

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': '172.31.24.145',  # Dirección IP privada del contenedor MySQL o el host
    'port': 8005,  # Puerto de la base de datos
    'user': 'root',
    'password': 'utec',
    'database': 'clinica_db'
}

# Función para obtener la conexión a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return connection

### --- CITAS --- ###

@app.route('/generarcita', methods=['POST'])
def crear_cita():
    data = request.get_json()
    campos = ['idpaciente', 'iddoctor', 'especialidad', 'fecha_hora', 'tipo']
    if not all(c in data for c in campos):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    idcita = data.get('idcita') or str(uuid.uuid4())
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO citas (idcita, idpaciente, iddoctor, especialidad, fecha_hora, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            idcita, data['idpaciente'], data['iddoctor'], data['especialidad'],
            data['fecha_hora'], data['tipo']
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Cita creada correctamente', 'idcita': idcita}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getcita/<idcita>', methods=['GET'])
def obtener_cita(idcita):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE idcita = %s", (idcita,))
    cita = cursor.fetchone()
    cursor.close()
    connection.close()
    if not cita:
        return jsonify({'message': 'Cita no encontrada', 'data': None}), 200
    return jsonify({'message': 'Cita encontrada', 'data': cita}), 200

@app.route('/getcita/paciente/<idpaciente>', methods=['GET'])
def obtener_citas_por_paciente(idpaciente):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE idpaciente = %s ORDER BY fecha_hora DESC", (idpaciente,))
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not citas:
        return jsonify({'message': 'No se encontraron citas para este paciente', 'data': []}), 200
    return jsonify({'message': 'Citas encontradas', 'data': citas}), 200

@app.route('/getcitas/doctor/<iddoctor>', methods=['GET'])
def obtener_citas_por_doctor(iddoctor):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE iddoctor = %s ORDER BY fecha_hora DESC", (iddoctor,))
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not citas:
        return jsonify({'message': 'No se encontraron citas para este doctor', 'data': []}), 200
    return jsonify({'message': 'Citas encontradas', 'data': citas}), 200

@app.route('/getcita/hoy', methods=['GET'])
def obtener_citas_hoy():
    hoy = datetime.now().strftime('%Y-%m-%d')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM citas WHERE DATE(fecha_hora) = %s", (hoy,))
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not citas:
        return jsonify({'message': 'No hay citas programadas para hoy', 'data': []}), 200
    return jsonify({'message': 'Citas para hoy encontradas', 'data': citas}), 200


### --- RECETAS --- ###

@app.route('/generarreceta', methods=['POST'])
def generar_receta():
    data = request.get_json()
    campos = ['idcita', 'fecha_emision', 'medicamentos', 'idpaciente', 'iddoctor', 'diagnostico', 'requiere_examen_medico']
    if not all(c in data for c in campos):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    idreceta = str(uuid.uuid4())
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
            data['fecha_emision'],
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
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recetas WHERE idpaciente = %s ORDER BY fecha_emision DESC", (idpaciente,))
    recetas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not recetas:
        return jsonify({'message': 'No se encontraron recetas para este paciente', 'data': []}), 200
    return jsonify({'message': 'Recetas encontradas', 'data': recetas}), 200

@app.route('/getrecetas/doctor/<iddoctor>', methods=['GET'])
def obtener_recetas_por_doctor(iddoctor):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recetas WHERE iddoctor = %s ORDER BY fecha_emision DESC", (iddoctor,))
    recetas = cursor.fetchall()
    cursor.close()
    connection.close()
    if not recetas:
        return jsonify({'message': 'No se encontraron recetas para este doctor', 'data': []}), 200
    return jsonify({'message': 'Recetas encontradas', 'data': recetas}), 200

@app.route('/getreceta/cita/<idcita>', methods=['GET'])
def obtener_receta_por_cita(idcita):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recetas WHERE idcita = %s", (idcita,))
    receta = cursor.fetchone()
    cursor.close()
    connection.close()
    if not receta:
        return jsonify({'message': 'No hay receta asociada a esta cita', 'data': None}), 200
    return jsonify({'message': 'Receta encontrada', 'data': receta}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
