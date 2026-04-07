from flask import Flask, render_template, request, redirect, url_for
from cassandra.cluster import Cluster
import uuid

app = Flask(__name__)

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('universidad')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/estudiantes')
def index():
    rows = session.execute('SELECT * FROM estudiantes')
    return render_template('index.html', estudiantes=rows)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    carrera = request.form['carrera']
    email = request.form['email']
    nota = float(request.form['nota'])

    session.execute(
        'INSERT INTO estudiantes (id,nombre,carrera,email,nota,fecha_ingreso) VALUES (%s,%s,%s,%s,%s,toDate(now()))',
        (uuid.uuid4(), nombre, carrera, email, nota)
    )
    return redirect(url_for('index'))

@app.route('/eliminar/<string:id>', methods=['POST'])
def eliminar(id):
    session.execute(
        'DELETE FROM estudiantes WHERE id=%s',
        [uuid.UUID(id)]
    )
    return redirect(url_for('index'))

@app.route('/cursos/<string:id>')
def ver_cursos(id):
    cursos = session.execute(
        'SELECT * FROM cursos_por_estudiante WHERE estudiante_id=%s',
        [uuid.UUID(id)]
    )
    return render_template(
        'cursos.html',
        cursos=cursos,
        estudiante_id=id
    )

if __name__ == '__main__':
    app.run(debug=True)