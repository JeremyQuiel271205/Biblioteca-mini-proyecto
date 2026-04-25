from flask import *
from conexion.Conn import Conn
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL = Conn.mysql()
CURSOR = MYSQL.cursor()
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/', methods = ['GET', 'POST'])
def index():
    session.pop('logueado', None)
    session.pop('usuario', None)

    session.setdefault('mensaje_login', "") # Crea la session si no existe

    return render_template('index.html', mensaje = session.get('mensaje_login'))

@app.route('/registro/usuarios')
def registro_usuarios():
    session.setdefault('mensaje_registro_usuario', "")
    return render_template('registro_usuario.html', mensaje = session.get('mensaje_registro_usuario'))

@app.route('/registro/libros')
def registro_libros():
    return render_template('registro_libros.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contra = request.form.get('contra')
        
        if not (correo and contra):
            session['mensaje_login'] = f"ERROR: Llene todos los campos"
            return redirect(url_for('index'))

        try:
            CURSOR.execute("SELECT * FROM usuario WHERE correo = %s AND contra = %s;", (correo, contra))
            usuario = CURSOR.fetchone()

        except Exception as e:
            session['mensaje_login'] = f"ERROR buscar usuario: {e}"
            return redirect(url_for('index'))

        if usuario:
            session['usuario'] = {
                'id': usuario[0],
                'nombre': usuario[1],
                'apellido': usuario[2],
                'correo': usuario[3],
            } 

            session['logueado'] = True
            session.pop('mensaje_login', None)
            return redirect(url_for('usuario'))
        
        session['mensaje_login'] = 'USUARIO NO VALIDO: inserta bien los datos o registrate'
        return redirect(url_for('index'))
    
    session['mensaje_login'] = "ERROR METODO: el metodo no es POST"
    return redirect(url_for('index'))

@app.route('/usuario', methods = ['GET', 'POST'])
def usuario():
    if session.get('logueado'):
        return render_template('usuario.html', usuario = session.get('usuario'))
    return redirect(url_for('index'))

@app.route('/usuario/correo', methods = ['GET', 'POST'])
def usuario_correo():
    return render_template('usuario_correo.html')

@app.route('/usuario/prestamo')
def usuario_prestamo():
    return render_template('usuario_prestamo.html')

@app.route('/crear/usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contra = request.form.get('contra')
        tipo = request.form.get('tipo')
        becado = request.form.get('becado')
        es_becado = 1 if becado else 0
        carrera = request.form.get('carrera')
        asignatura = request.form.get('asignatura')
        

        if not (nombre and apellido and correo and contra and (carrera or asignatura)):
            session['mensaje_registro_usuario'] = "ERROR: Llene todos los campos"
            return redirect(url_for('registro_usuarios'))
        
        try:
            CURSOR.execute("SELECT * FROM usuario WHERE correo = %s", (correo))
            usuario = CURSOR.fetchone()
            

        except Exception as e:
            session['mensaje_registro_usuario'] = f"ERROR BASE DE DATOS: {e}"
            return redirect(url_for('registro_usuarios'))
        

        if usuario:
            session['mensaje_registro_usuario'] = f"ERROR: {correo} ya esta registrado, prueba otro correo o inicia sesion con este"
            return redirect(url_for('registro_usuarios'))


        try:
            CURSOR.execute("INSERT INTO usuario (nombre, apellido, correo, contra) VALUES (%s, %s, %s, %s)", (nombre, apellido, correo, contra))

            if tipo == "estudiante":
                CURSOR.execute("INSERT INTO estudiante (id_estudiante, becado, carrera) VALUES (last_insert_id(), %s, %s)", (es_becado, carrera))
            elif tipo == "profesor":
                CURSOR.execute("INSERT INTO profesor (id_profesor, asignatura) VALUES (last_insert_id(), %s)", (asignatura))
            else:
                session['mensaje_registro_usuario'] = "ERROR DE TIPO: no se identifico el tipo de usuario"

                return redirect(url_for('registro_usuarios'))
            
            MYSQL.commit() #guarda los cambios
            session['mensaje_registro_usuario'] = "Registro exitoso, inicia sesion ahora"

            return redirect(url_for('registro_usuarios'))
        except Exception as e:
            MYSQL.rollback() #Deshace los cambios si da error
            session['mensaje_registro_usuario'] = f"ERORR: {e}"

    session['mensaje_registro_usuario'] = "ERROR DE METODO: metodo no es POST"
    return redirect(url_for('index'))

@app.route('/crear/libros', methods=['GET', 'POST'])
def crear_libros():
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/volver')
def volver():
    return redirect(url_for('index'))

    
if __name__ == '__main__':
    app.run(debug=True)