from flask import *
from conexion.Conn import Conn
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL = Conn.mysql()
CURSOR = MYSQL.cursor()
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro_usuarios():
    return render_template('registro.html')

@app.route('/registro/libros')
def registro_libros():
    return render_template('registro_libros.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('usuario'))
    return redirect(url_for('index'))

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/usuario/correo')
def usuario_correo():
    return render_template('usuario_correo.html')

@app.route('/usuario/prestamo')
def usuario_prestamo():
    return render_template('usuario_prestamo.html')

@app.route('/registro/tipo/usuario', methods = ['GET', 'POST'])
def tipo_usuario():
    tipo = "estudiante" #ejemplo

    if tipo == "estudiante":
        return render_template('tipo_estudiante.html')
    elif tipo == "profesor":
        return render_template('tipo_profesor.html')
if __name__ == '__main__':
    app.run(debug=True)