from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# # inicializamos SQLAlchemy para usarlo en models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:asdasd@localhost/g20_tdp2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # blueprint para las rutas con autenticacion
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint para las rutas publicas
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app