from flask import Flask, request
#import logging


#from flask import render_template
app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    #app.logger.info('Info')
    return 'Pagina de Index'

@app.route('/poster',methods=["GET"])
def poster():
    if request.method=="GET":
        try:
            temp=request.args.get("temp")
            vol=request.args.get("vol")
            id=request.args.get("id")
            time=request.args.get("time")
            respuesta='Id={}<br/>Time={}<br/>Temperatura={}<br/>Volumen={}'.format(str(id),str(time),str(float(temp)),str(float(vol)))
            return respuesta
        except:
            return "get simple"
    else:
        return "falla"

# if __name__=="__main__":
#     app.run(host="0.0.0.0",debug="True")
#     import logging
#     app.logger.INFO('asd')
#     logging.basicConfig(filename='errossr.log',level=logging.INFO)

    