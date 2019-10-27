from flask import Blueprint, render_template, request
from .models import Usuario, Datos, Nodo
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.razonSocial)

@main.route("/mostrar")
def mostrar():
    return render_template('show_all.html', tabla=Datos.query.all(), nodos=Nodo.query.all() )

@main.route('/poster', methods=["GET"])
def poster():
    #/poster?nodo=4&timestamp=2019-10-09%2018:59:00&temp=20.00&vol=0.00&lat=34.91&long=57.96&evento=0
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

@main.route('/postjson', methods = ['POST'])
def postJsonHandler():
    content = request.get_json()
    var1 = content.get("sensorType")
    var2 = content.get("values")
    var3 = content.get("timestamps")
    print (var1)
    print (var2)
    print (var3)
    return 'JSON posted'