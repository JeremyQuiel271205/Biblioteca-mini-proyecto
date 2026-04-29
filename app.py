from flask import *
from routes.auth import auth_bp
from routes.libros import libros_bp


app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(libros_bp)

if __name__ == '__main__':
    app.run(debug=True)