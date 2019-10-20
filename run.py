from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from basedatos import db, Datos, Nodo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:asdasd@localhost/g20_tdp2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/mostrar")
def mostrar():
    return render_template('show_all.html', tabla=Datos.query.all(),nodos=Nodo.query.all() )

@app.route('/poster', methods=["GET"])
def poster():
    #nodo=4&timestamp=%222019-10-09%2018:59:00%22&temp=20.00&vol=0.00&lat=34.91&long=57.96&evento=0
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

@app.route('/version', methods=["GET"])
def version():
    #nodo=4&timestamp=%222019-10-09%2018:59:00%22&temp=20.00&vol=0.00&lat=34.91&long=57.96&evento=0
    nodo = request.args.get("nodo")
    print(nodo)
    firm = request.args.get("firmware")
    print(firm)
    time = request.args.get("timestamp")
    print(time)
    # nodo_act = db.session.query(Nodo).filter(Nodo.id == nodo)
    # nodo_act.firmware = firm
    # nodo_act.timestamp_fm = time
    # db.session.commit()
    nodo_act = Nodo.query.get(1)
    nodo_act.firmware = firm
    nodo_act.timestamp_fm = time
    db.session.add(nodo_act)
    db.session.commit()

if __name__=="__main__":
    app.run(debug="True")
#     import logging
#     app.logger.INFO('asd')
#     logging.basicConfig(filename='errossr.log',level=logging.INFO)

    #app.run(host= '192.168.1.105',port=80,debug="True")