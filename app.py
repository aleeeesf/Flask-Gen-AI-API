import os
from flask import Flask
from config import Config
from extensions import db, jwt
from routes import auth_bp, chat_bp

basedir = os.path.abspath(os.path.dirname(__file__))

def start():
    """ Iniciar la aplicación """
    app = Flask(__name__)
    config = Config()

    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

    # Iniciar base de datos y JWT
    db.init_app(app)
    jwt.init_app(app)

    # Registrar endpoints de autenticación y del chat
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    with app.app_context():
        db.create_all()

    return app

# Situado afuera para ser detectado por guinicorn
app = start()
# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)