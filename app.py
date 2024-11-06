from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Función para conectar a la base de datos
def connect_db():
    connection = mysql.connector.connect(
        host='localhost',
        port=8080,  
        user='root', 
        password='puenteMOREno910$',  
        database='pruebaaa'  
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

# Obtener todos los alumnos (GET)
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")  
    alumnos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(alumnos)

# Obtener un alumno por su ID (GET)
@app.route('/alumnos/<int:id_alumno>', methods=['GET'])
def get_alumno(id_alumno):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos WHERE id = %s", (id_alumno,))
    alumno = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if alumno:
        return jsonify(alumno)
    else:
        return jsonify({"Error": "No se encontró al alumno"}), 404

# Agregar un nuevo alumno (POST)
@app.route('/alumnos', methods=['POST'])
def add_alumno():
    connection = connect_db()
    cursor = connection.cursor()

    # Obtener datos del request
    nombre = request.form.get('name')
    carrera = request.form.get('carrera')
    edad = request.form.get('edad')

    # Validar que no sean None
    if not nombre or not carrera or edad is None:
        return jsonify({"error": "Datos incompletos"}), 400

    # Insertar en la tabla
    query = "INSERT INTO alumnos (name, carrera, edad) VALUES (%s, %s, %s)"
    values = (nombre, carrera, edad)
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
    return redirect(url_for('index'))

# Actualizar un alumno existente (PUT)
@app.route('/alumnos/<int:id_alumno>', methods=['PUT'])
def update_alumno(id_alumno):
    connection = connect_db()
    cursor = connection.cursor()

    # Obtener datos del request
    data = request.get_json()
    nombre = data.get('name')
    carrera = data.get('carrera')
    edad = data.get('edad')

    # Validar que no sean None
    if not nombre or not carrera or edad is None:
        return jsonify({"error": "Datos incompletos"}), 400

    # Actualizar en la tabla
    query = "UPDATE alumnos SET name = %s, carrera = %s, edad = %s WHERE id = %s"
    values = (nombre, carrera, edad, id_alumno)
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"success": True})

# Eliminar un alumno (DELETE)
@app.route('/alumnos/<int:id_alumno>', methods=['DELETE'])
def delete_alumno(id_alumno):
    connection = connect_db()
    cursor = connection.cursor()

    # Eliminar de la tabla
    cursor.execute("DELETE FROM alumnos WHERE id = %s", (id_alumno,))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
