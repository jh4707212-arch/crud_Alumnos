import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 

# Cargar las variables de entorno 
load_dotenv()

# Crear instancia
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
# 🛑 CORRECCIÓN 1: La función os.getenv() debe recibir la clave de la variable 
# de entorno (ej. 'DATABASE_URL'), no el valor completo de la URI. El valor 
# completo debe estar en un archivo .env.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# NOTA: Asegúrate de tener un archivo .env con: DATABASE_URL='postgresql://juan:...'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Modelo de la base de datos
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return{
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre,
        }


# Ruta raiz
@app.route('/')
def index():
    # Trae todos los estudiantes
    estudiantes = Estudiante.query.all()
    return render_template('index.html', estudiantes = estudiantes)

# Ruta /estudiantes/new para crear un nuevo estudiante
@app.route('/estudiantes/new', methods=['GET','POST'])
def create_estudiante():
    if request.method == 'POST':
        # Agregar Estudiante
        no_control = request.form['no_control']
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        ap_materno = request.form['ap_materno']
        # 💡 MEJORA 1: Convertir el semestre a entero antes de usarlo en el modelo
        semestre = int(request.form['semestre']) 

        nvo_estudiante = Estudiante(no_control=no_control, nombre=nombre, ap_paterno=ap_paterno, ap_materno= ap_materno, semestre= semestre)

        db.session.add(nvo_estudiante)
        db.session.commit()

        return redirect(url_for('index'))
    
    # Aqui sigue si es GET
    return render_template('create_estudiante.html')


# Eliminar estudiante
@app.route('/estudiantes/delete/<string:no_control>')
def delete_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
    return redirect(url_for('index'))

# Actualizar estudiante
@app.route('/estudiantes/update/<string:no_control>', methods=['GET','POST'])
# 🛑 CORRECCIÓN 2: Cambiar el nombre de la función y la variable para consistencia
# y para evitar un error de "Alumno is not defined".
def update_estudiante(no_control):
    # Usar el modelo Estudiante que sí existe
    estudiante = Estudiante.query.get(no_control) 
    
    if estudiante is None:
        # Manejar caso si el estudiante no existe
        return "Estudiante no encontrado", 404

    if request.method == 'POST':
        # Usar la variable 'estudiante' para actualizar los datos
        estudiante.nombre = request.form['nombre']
        estudiante.ap_paterno = request.form['ap_paterno']
        estudiante.ap_materno = request.form['ap_materno']
        # 💡 MEJORA 2: Convertir a entero al actualizar
        estudiante.semestre = int(request.form['semestre'])
        
        db.session.commit()
        return redirect(url_for('index'))
    # Usar la variable 'estudiante' y el nombre de plantilla consistente
    return render_template('update_estudiante.html', estudiante=estudiante) 


# Ruta /alumnos (Para consistencia se recomienda cambiar a /estudiantes)
@app.route('/alumnos')
def getAlumnos():
    return 'Aqui van los alumnos'


if __name__ == '__main__':
    # Usar 'flask run' es preferible en desarrollo. 
    app.run(debug=True)