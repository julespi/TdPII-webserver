from flask import Blueprint, render_template, request
from .models import Datos, Nodo
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/poster', methods=["GET"])
def poster():
    # /poster?nodo=4&timestamp=2019-10-09%2018:59:00&temp=20.00&vol=0.00&lat=34.91&long=57.96&evento=0
    nodo = request.args.get("nodo")
    time = request.args.get("timestamp")
    vol = request.args.get("vol")
    temp = request.args.get("temp")
    lat = request.args.get("lat")
    lon = request.args.get("long")
    evento = request.args.get("evento")
    algo = Datos(nodo, time, vol, temp, lat, lon, evento)
    db.session.add(algo)
    db.session.commit()
    return "listo"


@main.route('/postjson', methods=['POST'])
def postJsonHandler():
    content = request.get_json()
    var1 = content.get("sensorType")
    var2 = content.get("values")
    var3 = content.get("timestamps")
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
