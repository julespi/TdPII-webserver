from flask import Flask, request
#from flask import render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return 'Pagina de Index'

@app.route('/poster',methods=["GET"])
def poster():
    if request.method=="GET":
        try:
            temp=request.args.get("temp")
            vol=request.args.get("vol")
            respuesta='Temperatura={}<br/>Volumen={}'.format(str(float(temp)),str(float(vol)))
            return respuesta
        except:
            return "get simple"
    else:
        return "falla"