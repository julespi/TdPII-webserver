from flask import (
    Blueprint,
    render_template,
    request
)
from .models import (
    Dato,
    Nodo,
    Usuario
)
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from . import db

main = Blueprint('main', __name__)


@main.route('/initdb')
def init_db():
    # Inicializacion de la bd. Se crea lo minimo y necesario para la
    # visualizacion del sitio web.

    # Se destruyen las tablas existentes.
    db.drop_all()
    # Se crean las tablas en base a los modelos definidos en "models.py".
    db.create_all()
    # Creamos un usuario.
    admin = Usuario(
        email="admin@admin.com",
        razonSocial="TDPII G20",
        contrasenia=generate_password_hash(
            "admin",
            method='sha256'
        )
    )
    # Creamos un dato.
    dato_demo = Dato(
        timestamp=datetime.now(),
        volumen=123.45,
        temperatura=21.5,
        latitud=-34.9072021,
        longitud=-57.9605293,
        evento="0"
    )
    # Creamos un nodo.
    nodo_demo = Nodo(
        nodo=10,
        firmware="factory_fm",
        timestamp_fm=datetime.now(),
        nombre="Nodo Demo",
        descripcion="Nodo para demo TdPII - G20 - 2019"
    )
    # Le asignamos el dato al nodo.
    nodo_demo.datos.append(dato_demo)
    # Le asignamos el nodo al usuario.
    admin.nodos.append(nodo_demo)
    # agregamos a la sesion el usuario. El nodo y el dato seran agregados
    # automaticamente debido a la relacion que exite entre ambos.
    db.session.add(admin)
    # Haciendo "commit", insertaremos los registros en las tablas
    # correspondientes.
    db.session.commit()
    # Retornamos un simple mensaje de confirmacion.
    return ('base de datos creada')


@main.route('/initdbdemo')
def init_db_demo():
    # Inicializacion de la bd para la muestra. Se crea lo necesario para la
    # correcta visualizacion del sitio web para la demostracion del proyecto.
    # No se documentara en detalle lo que ocurre en esta funcion debido a que
    # es similar a la anterior.

    db.drop_all()
    db.create_all()
    usuario1 = Usuario(
        email="usuario1@empresa1.com",
        razonSocial="EMPRESA 1 SA",
        contrasenia=generate_password_hash(
            "usuario1",
            method='sha256'
        )
    )
    usuario2 = Usuario(
        email="usuario2@empresa2.com",
        razonSocial="EMPRESA 2 SA",
        contrasenia=generate_password_hash(
            "usuario2",
            method='sha256'
        )
    )
    dato_demo1 = Dato(
        timestamp=datetime.now(),
        volumen=123.45,
        temperatura=21.5,
        latitud=-34.9072021,
        longitud=-57.9605293,
        evento="0"
    )
    dato_demo2 = Dato(
        timestamp=datetime.now(),
        volumen=132.54,
        temperatura=22.3,
        latitud=-34.9072021,
        longitud=-57.9605293,
        evento="0"
    )
    nodo_demo1 = Nodo(
        nodo=10,
        firmware="factory_fm",
        timestamp_fm=datetime.now(),
        nombre="Nodo Demo 1",
        descripcion="Nodo para demo TdPII - G20 - 2019"
    )
    nodo_demo2 = Nodo(
        nodo=11,
        firmware="factory_fm",
        timestamp_fm=datetime.now(),
        nombre="Nodo Demo 2",
        descripcion="Nodo para demo TdPII - G20 - 2019"
    )
    nodo_demo1.datos.append(dato_demo1)
    nodo_demo2.datos.append(dato_demo2)
    usuario1.nodos.append(nodo_demo1)
    usuario1.nodos.append(nodo_demo2)
    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.commit()
    return ('base de datos creada')


@main.route('/')
def index():
    # Pagina de inicio

    return render_template('index.html')


@main.route('/poster', methods=["GET"])
def poster():
    # Esta es la URL a la que el nodo le solicita la peticion para la
    # insercion de los datos en la bd. La estructura de la peticion
    # sera como la siguiente:
    # /poster?nodo=4&timestamp=2019-10-09%2018:59:00&temp=20.00&vol=0.00&lat=34.91&long=57.96&evento=0

    # Obtengo los datos de los argumentos de la peticion GET.
    nod = request.args.get("nodo")
    time = request.args.get("timestamp")
    date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
    """timestamp = time[0].split("-")
    timestamp += time[1].split(":")
    segundo = int(timestamp[5])
    print(timestamp[0])
    print(timestamp[1])
    print(timestamp[2])
    print(timestamp[3])
    print(timestamp[4])
    print(segundo)
    print(type(segundo))"""
    """
    date = datetime(
        year=timestamp[0],
        month=timestamp[2],
        day=timestamp[1],
        hour=timestamp[3],
        minute=timestamp[4],
        second=segundo
    )"""
    vol = request.args.get("vol")
    temp = request.args.get("temp")
    lat = request.args.get("lat")
    lon = request.args.get("long")
    evento = request.args.get("evento")
    # Obtengo de la bd, el nodo que transmitio los datos.
    nodo = db.session.query(Nodo).filter(Nodo.nodo == nod).first()
    # Creo un objeto "dato" a partir de los argumentos.
    nuevo_dato = Dato(
        id_nodo=nodo.id,
        timestamp=date,
        volumen=vol,
        temperatura=temp,
        latitud=lat,
        longitud=lon,
        evento=evento
    )
    # Inserto el nuevo dato
    db.session.add(nuevo_dato)
    db.session.commit()
    return "Dato recibido"


@main.route('/postjson', methods=['POST'])
def postJsonHandler():
    # Funcion de prueba para el manejo de datos con formato JSON

    content = request.get_json()
    var1 = content.get("clave")
    var2 = content.get("values")
    var3 = content.get("timestamps")
    print(var1)
    return 'JSON posted'


@main.route('/version', methods=["GET"])
def version():
    # Funcion que se encarga de dejar registro del firmware del nodo. El nodo
    # realizara un request con la informacion de su firmware cada vez que
    # se inicie. El formato del request sera como el siguiente:
    # /version?nodo=10&timestamp=0000-00-00%2000:00:00&firmware=20190611"

    # Obtengo los datos pasados por el request
    nodo_local = request.args.get("nodo")
    firm = request.args.get("firmware")
    time = request.args.get("timestamp")
    # Obtengo el nodo que realizo dicho request
    nodo_act = db.session.query(Nodo).filter_by(nodo=nodo_local).first()
    # Modifico los datos e inserto en la bd
    nodo_act.firmware = firm
    nodo_act.timestamp_fm = time
    db.session.commit()
    return "Firmware actualizado"
