from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Usuario, Nodo, Dato, datos_schema
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    usuario = Usuario.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed
    # password in database
    if not usuario or not check_password_hash(usuario.contrasenia, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right
    # credentials
    login_user(usuario, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.razonSocial, nodos=Nodo.query.filter_by(id_cliente=current_user.id))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get("email")
    razon_social = request.form.get("razonSocial")
    password = request.form.get("password")

    # if this returns a user, then the email already exists in database
    usuario = Usuario.query.filter_by(email=email).first()

    """ if usuario:  # if a user is found, we want to redirect back to signup
        page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup')) """

    # create new user with the form data. Hash the password so plaintext
    # version isn't saved.
    new_user = Usuario(email=email, razonSocial=razon_social,
                       contrasenia=generate_password_hash(password,
                       method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/mostrar", methods=["GET"])
@login_required
def mostrar():
    return render_template("show_all.html")


@auth.route("/mostrar", methods=["POST"])
@login_required
def mostrar_post():
    # lista_de_nodos = Nodo.query.filter_by(cliente=current_user.id).with_entities(Nodo.nodo).all()
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
    payload = datos_schema.dump(datos)
    # tabla=Datos.query.filter(Datos.nodo.in_(lista_de_nodos)), nodos=Nodo.query.filter_by(cliente=current_user.id)
    return jsonify(payload)
