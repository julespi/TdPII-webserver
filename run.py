from flask import Flask, request
from flask_mysqldb import MySQL
#import logging


#from flask import render_template
#mysql = MySQL()
app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = 'usuario'
app.config['MYSQL_PASSWORD'] = 'asdasd'
app.config['MYSQL_DB'] = 'db_prueba'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    #app.logger.info('Info')
    return 'Pagina de Index'

@app.route("/prueba")
def prueba():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tabla1(id_nodo,volumen,temperatura) VALUES (1,56.58,12.3)")
    mysql.connection.commit()
    cur.close()
    return "Listo"

@app.route('/poster',methods=["GET"])
def poster():
    if request.method=="GET":
        #try:
        id=request.args.get("id")
        if id is None:
            id = 0
        time=request.args.get("timestamp")
        if time is None:
            time=str("\"1999-01-01 00:00:00\"")
        vol=request.args.get("vol")
        if vol is None:
            vol=0.00
        temp=request.args.get("temp")
        if temp is None:
            temp=0.00
        lat=request.args.get("latitud")
        if lat is None:
            lat=0.00
        lon=request.args.get("longitud")
        if lon is None:
            lon=0.00
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tabla1(id_nodo,timestamp,volumen,temperatura,latitud,longitud) VALUES ({},{},{},{},{},{})".format(int(id),str(time),float(vol),float(temp),float(lat),float(lon)))
        mysql.connection.commit()
        cur.close()
        return "OK"
        #except:
            #return "get simple"
    else:
        return "falla"

if __name__=="__main__":
    app.run(host= '192.168.1.105',port=80,debug="True")
#     import logging
#     app.logger.INFO('asd')
#     logging.basicConfig(filename='errossr.log',level=logging.INFO)

    