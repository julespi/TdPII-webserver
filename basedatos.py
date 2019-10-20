from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Float, Integer, String

db = SQLAlchemy()

class Datos(db.Model):
    __tablename__ = 'datos'
    #id_nodo,timestamp,volumen,temperatura,latitud,longitud
    id = db.Column("id", db.INTEGER, primary_key=True)
    nodo = db.Column("id_nodo", db.INTEGER)
    time = db.Column("timestamp", db.DATETIME)
    vol = db.Column("volumen", db.Numeric(5,3))
    temp = db.Column("temperatura", db.Numeric(3,3))
    lat = db.Column("latitud", db.Numeric(2,10))
    lon = db.Column("longitud", db.Numeric(2,10))
    eve = db.Column("evento", String(2))


    def __init__(self, nodo, time, vol, temp, lat, lon, eve):
        self.nodo = nodo
        self.time = time
        self.vol = vol
        self.temp = temp
        self.lat = lat
        self.lon = lon
        self.eve = eve

class Nodo(db.Model):
    __tablename__ = 'nodo'
    id = db.Column("id", db.INTEGER, primary_key=True)
    nodo = db.Column("nodo", db.INTEGER)
    cliente = db.Column("id_cliente", db.INTEGER)
    firmware = db.Column("firmware", String(10))
    nombre = db.Column("nombre", String(50))
    descripcion = db.Column("descripcion", String(100))


    def __init__(self, nodo, cliente, firmware, nombre, descripcion):
        self.nodo = nodo
        self.cliente = cliente
        self.firmware = firmware
        self.nombre = nombre
        self.descripcion = descripcion