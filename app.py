from flask import *
from conexion.Conn import Conn
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL = Conn.mysql()
CURSOR = MYSQL.cursor()
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/registro/usuarios')
def registro_usuarios():
    return render_template('registro_usuario.html')

@app.route('/registro/libros')
def registro_libros():
    return render_template('registro_libros.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('usuario'))
    return redirect(url_for('index'))

@app.route('/usuario', methods = ['GET', 'POST'])
def usuario():
    return render_template('usuario.html')

@app.route('/usuario/correo', methods = ['GET', 'POST'])
def usuario_correo():
    return render_template('usuario_correo.html')

@app.route('/usuario/prestamo')
def usuario_prestamo():
    return render_template('usuario_prestamo.html')

@app.route('/crear/usuario', methods=['GET', 'POST'])
def crear_usuario():
    return redirect(url_for('index'))

@app.route('/crear/libros', methods=['GET', 'POST'])
def crear_libros():
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/volver')
def volver():
    return redirect(url_for('usuario'))
    
if __name__ == '__main__':
    app.run(debug=True)