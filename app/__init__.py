from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    # Funcion que se encarga de crear la instancia app

    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # blueprint para las rutas con autenticacion
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint para las rutas publicas
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
