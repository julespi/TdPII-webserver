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
        temp=request.args.get("temp")
        vol=request.args.get("vol")
        id=request.args.get("id")
        time=request.args.get("times")
        lat=request.args.get("latitud")
        lon=request.args.get("longitud")
        #respuesta='Id={}<br/>Time={}<br/>Temperatura={}<br/>Volumen={}'.format(str(id),str(time),str(float(temp)),str(float(vol)))
        cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO tabla1(id_nodo,timestamp,volumen,temperatura,latitud,longitud)\
                #VALUES ({},{},{},{},{},{})".format(int(id),str(time),float(str(vol)),float(str(temp)),float(str(lat)),float(str(lon))))
        cur.execute("INSERT INTO tabla1(id_nodo,timestamp) VALUES ({},{})".format(int(id),str(time)))
        mysql.connection.commit()
        cur.close()
        return "respuesta"
        #except:
            #return "get simple"
    else:
        return "falla"

if __name__=="__main__":
    app.run(host= '192.168.1.105',port=5000,debug="True")
#     import logging
#     app.logger.INFO('asd')
#     logging.basicConfig(filename='errossr.log',level=logging.INFO)

    