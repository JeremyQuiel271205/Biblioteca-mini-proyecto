from flask import *
from conexion.Conn import Conn
import os
from dotenv import load_dotenv
from datetime import date, timedelta

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
    session.pop('mensaje_registro_usuario', None)
    session.pop('mensaje_registro_libro', None)
    session.pop('mensaje_prestamo', None)

    session.setdefault('mensaje_login', "") # Crea la session si no existe

    return render_template('index.html', mensaje = session.get('mensaje_login'))

@app.route('/registro/usuarios')
def registro_usuarios():
    session.setdefault('mensaje_registro_usuario', "")
    return render_template('registro_usuario.html', mensaje = session.get('mensaje_registro_usuario'))

@app.route('/registro/libros')
def registro_libros():
    session.setdefault('mensaje_registro_libro', "")
    return render_template('registro_libros.html', mensaje = session.get('mensaje_registro_libro'))

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
    if not session.get('logueado'):
        return redirect(url_for('index'))
    
    session.setdefault('mensaje_prestamo', "")

    try:
        CURSOR.execute("SELECT id_libro, nombre_libro, nombre_autor, apellido_autor, precio_base FROM libro WHERE estado = 1")
        lista = CURSOR.fetchall()
    except Exception as e:
        return render_template('usuario_prestamo.html', mensaje = session.get('mensaje_prestamo'), codigo_mensaje = "error", e = e)
    
    if not lista:
        return render_template('usuario_prestamo.html', mensaje = session.get('mensaje_prestamo'), codigo_mensaje = "vacia")
    
    return render_template('usuario_prestamo.html', mensaje = session.get('mensaje_prestamo'), codigo_mensaje = "lista", lista = lista)

@app.route('/crear/usuario', methods=['POST'])
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

@app.route('/crear/libros', methods=['POST'])
def crear_libros():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        precio = request.form.get('precio')

        if not (titulo and nombre and precio):
            session['mensaje_registro_libro'] = "ERROR: Llene todos los campos obligatorios"
            return redirect(url_for('registro_libros'))
        
        try:
            CURSOR.execute("SELECT * FROM libro WHERE nombre_libro = %s and nombre_autor = %s",(titulo, nombre))

            libro = CURSOR.fetchone()

            if libro:
                session['mensaje_registro_libro'] = f"{titulo} de {nombre} {apellido} ya esta registrado"
                return redirect(url_for('registro_libro'))
            
        except Exception as e:
            session['mensaje_registro_libro'] = f"ERORR BUSQUEDA: {e}"
            return redirect(url_for('registro_libros'))
        

        try:
            CURSOR.execute('INSERT INTO libro (nombre_libro, nombre_autor, apellido_autor, precio_base) VALUES (%s, %s, %s, %s)',(titulo, nombre, apellido, precio))

            MYSQL.commit()

            session['mensaje_registro_libro'] = "Se registro el libro correctamente"
            return redirect(url_for('registro_libros'))
        except Exception as e:
            MYSQL.rollback()

            session['mensaje_registro_libro'] = f"ERRO INSERTO: {e}"
            return redirect(url_for('registro_libros'))

    return redirect(url_for('registro_libros'))

@app.route('/crear/prestamo', methods = ['POST'])
def crear_prestamo():
    if request.method == 'POST' and session.get('logueado'):
        id_libro = request.form.get('id_libro')

        if not id_libro:
            session['mensaje_prestamo'] = "ERROR: Llene el campo"
            return redirect(url_for('usuario_prestamo'))
        
        try:
            CURSOR.execute("SELECT * FROM libro WHERE id_libro = %s",(id_libro))

            libro = CURSOR.fetchone()

            if not libro:
                session['mensaje_prestamo'] = f"Este ID de libro no esta registrado"
                return redirect(url_for('usuario_prestamo'))
            
        except Exception as e:
            session['mensaje_prestamo'] = f"ERORR BUSQUEDA: {e}"
            return redirect(url_for('usuario_prestamo'))
        
        usuario = session.get('usuario')

        fecha_actual = date.today()
        fecha_fin = fecha_actual + timedelta(days=30)

        try:
            CURSOR.execute('INSERT INTO prestamo (id_usuario, id_libro, fecha_fin) VALUES (%s, %s, %s)',(usuario['id'], id_libro, fecha_fin))
            CURSOR.execute('UPDATE libro SET estado = 0 WHERE id_libro = %s', (id_libro))
            MYSQL.commit()

            session['mensaje_prestamo'] = "Prestamo creado correctamente"
            return redirect(url_for('usuario_prestamo'))
        except Exception as e:
            MYSQL.rollback()

            session['mensaje_prestamo'] = f"ERRO INSERTO: {e}"
            return redirect(url_for('usuario_prestamo'))

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/volver')
def volver():
    session.pop('mensaje_login', None)
    return redirect(url_for('index'))

    
if __name__ == '__main__':
    app.run(debug=True)