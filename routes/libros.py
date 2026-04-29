from flask import * 

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/registrar/libro')
def registrar_libro():
    return render_template('libros/registrar_libro.html')

@libros_bp.route('/crear/libro')
def crear_libro():
    return render_template('libros/crear_libro.html')