from flask import Flask, request, render_template
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:asdasd@localhost/db_prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Datos(db.Model):
    __tablename__ = 'tabla1'
    #id_nodo,timestamp,volumen,temperatura,latitud,longitud
    id=db.Column("id",db.INTEGER, primary_key=True)
    nodo=db.Column("nodo",db.INTEGER)
    time=db.Column("timestamp",db.DATETIME)
    vol=db.Column("volumen",db.Numeric(5,3))
    temp=db.Column("temperatura",db.Numeric(3,3))
    lat=db.Column("latitud",db.Numeric(1,10))
    lon=db.Column("longitud",db.Numeric(1,10))


    def __init__(self,nodo,time,vol,temp,lat,lon):
        self.nodo=nodo
        self.time=time
        self.vol=vol
        self.temp=temp
        self.lat=lat
        self.lon=lon      

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/mostrar")
def mostrar():
    return render_template('show_all.html', tabla = Datos.query.all() )

@app.route('/poster',methods=["GET"])
def poster():
    nodo=request.args.get("id")
    time=request.args.get("timestamp")
    vol=request.args.get("vol")
    temp=request.args.get("temp")
    lat=request.args.get("lat")
    lon=request.args.get("lon")
    algo=Datos(nodo,time,vol,temp,lat,lon)
    db.session.add(algo)
    db.session.commit()
    return "listo"

if __name__=="__main__":
    app.run(debug="True")
#     import logging
#     app.logger.INFO('asd')
#     logging.basicConfig(filename='errossr.log',level=logging.INFO)

    #app.run(host= '192.168.1.105',port=80,debug="True")