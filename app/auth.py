from flask import (
    Blueprint,
    render_template,
    redirect, url_for,
    request,
    flash,
    jsonify
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from .models import (
    Usuario,
    Nodo,
    Dato,
    datos_schema
)
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    # Pagina para el inicio de sesion.

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # Toda informacion registrada en el form del inicio de sesion es atajada
    # por esta funcion.

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    # Busco el usuario que esta tratando de iniciar sesion.
    usuario = Usuario.query.filter_by(email=email).first()
    # Si no existe, emito un flash.
    if not usuario or not check_password_hash(usuario.contrasenia, password):
        flash('Usuario o contraseña incorrecto.')
        return redirect(url_for('auth.login'))
    # Si el usuario existe, queda registrado con el modulo login_user.
    login_user(usuario, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/profile')
@login_required
def profile():
    # Pagina del perfil del usuario.

    return render_template('profile.html',
                           nombre=current_user.razonSocial,
                           email=current_user.email,
                           nodos=Nodo.query.filter_by(
                               id_cliente=current_user.id)
                           )


@auth.route('/signup')
def signup():
    # Pagina para el registro de un nuevo usuario.

    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # Toda informacion registrada en el form del registro de un nuevo usuario
    # es atajada por esta funcion.

    # Obtengo los datos del form.
    email = request.form.get("email")
    razon_social = request.form.get("razonSocial")
    password = request.form.get("password")

    # Busco si el usuario ya existe.
    usuario = Usuario.query.filter_by(email=email).first()
    # Si el usuario existe, se le advierte.
    if usuario:
        flash('Usuario ya registrado!')
        return redirect(url_for('auth.signup'))

    # Se crea un usuario nuevo con los datos provistos.
    new_user = Usuario(
        email=email,
        razonSocial=razon_social,
        contrasenia=generate_password_hash(password, method='sha256')
    )
    # Insertamos el nuevo usuario en la bd.
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    # Funcion que se encarga del cierre de sesion.

    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/mostrar", methods=["GET"])
@login_required
def mostrar():
    # Pagina que se encarga de mostrar todos los datos registrados
    # por los nodos.

    return render_template("show_all.html")


@auth.route("/mostrar", methods=["POST"])
@login_required
def mostrar_post():
    # Esta funcion se encarga de enviar los datos solicitados por AJAX para
    # poder mostrar los datos registrados por los nodos.

    # Obtengo los datos que necesito mostrar para el cliente logueado.
    datos = db.session.query(
        Nodo.nombre,
        Dato.timestamp,
        Dato.volumen,
        Dato.temperatura,
        Dato.latitud,
        Dato.longitud,
        Dato.evento
    ).filter(
        Nodo.id_cliente == current_user.id,
        Dato.id_nodo == Nodo.id
    ).all()
    # Formateo el resultado para que pueda ser convertido a JSON.
    payload = datos_schema.dump(datos)
    return jsonify(payload)
