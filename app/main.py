from flask import Blueprint, render_template, request
from .models import Dato, Nodo, Usuario
from datetime import datetime
from werkzeug.security import generate_password_hash
from . import db

main = Blueprint('main', __name__)


@main.route('/initdb')
def init_db():
    db.drop_all()
    db.create_all()
    admin = Usuario(
        email="admin@admin.com",
        razonSocial="TDPII G20",
        contrasenia=generate_password_hash(
            "admin",
            method='sha256'
        )
    )
    dato_demo = Dato(
        timestamp=datetime.now(),
        volumen=123.45,
        temperatura=21.5,
        latitud=-34.9072021,
        longitud=-57.9605293,
        evento="0"
    )
    nodo_demo = Nodo(
        nodo=10,
        firmware="factory_fm",
        timestamp_fm=datetime.now(),
        nombre="Nodo Demo",
        descripcion="Nodo para demo TdPII - G20 - 2019"
    )
    nodo_demo.datos.append(dato_demo)
    admin.nodos.append(nodo_demo)
    db.session.add(admin)
    db.session.commit()
    
    return ('base de datos creada')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/poster', methods=["GET"])
def poster():
    # /poster?nodo=4&timestamp=2019-10-09%2018:59:00&temp=20.00&vol=0.00&lat=34.91&long=57.96&evento=0
    nod = request.args.get("nodo")
    time = request.args.get("timestamp")
    vol = request.args.get("volu")
    temp = request.args.get("temp")
    lat = request.args.get("lat")
    lon = request.args.get("long")
    evento = request.args.get("evento")
    nodo = db.session.query(Nodo).filter(Nodo.nodo == nod).first()
    algo = Dato(
        id_nodo=nodo.id,
        timestamp=time,
        volumen=vol,
        temperatura=temp,
        latitud=lat,
        longitud=lon,
        evento=evento)
    db.session.add(algo)
    db.session.commit()
    return "listo"


@main.route('/postjson', methods=['POST'])
def postJsonHandler():
    content = request.get_json()
    var1 = content.get("clave")
    var2 = content.get("values")
    var3 = content.get("timestamps")
    print (var1)
    return 'JSON posted'


@main.route('/version', methods=["GET"])
def version():
    # /version?nodo=10&timestamp=0000-00-00%2000:00:00&firmware=20190611"
    nodo_local = request.args.get("nodo")
    firm = request.args.get("firmware")
    time = request.args.get("timestamp")
    nodo_act = db.session.query(Nodo).filter_by(nodo=nodo_local).first()
    print(nodo_act.firmware)
    print(nodo_act.nodo)
    print(nodo_act.timestamp_fm)
    nodo_act.firmware = firm
    nodo_act.timestamp_fm = time
    # db.session.add(nodo_act)
    print(nodo_act.firmware)
    print(nodo_act.nodo)
    print(nodo_act.timestamp_fm)
    db.session.commit()
    return "holamanola"
