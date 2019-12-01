from . import db, ma
from sqlalchemy import Table, Column, Float, Integer, String, ForeignKey, func
from flask_login import UserMixin
from datetime import datetime
from marshmallow import fields


class Dato(db.Model):
    # Modelo de la tabla "dato".

    __tablename__ = 'dato'
    # Identificador
    id = db.Column("id", db.Integer, primary_key=True)
    # Clave foranea del nodo que inyecto el dato.
    id_nodo = db.Column(db.Integer, db.ForeignKey("nodo.id"))
    # Momento en el que el dato fue adquirido.
    timestamp = db.Column("timestamp", db.DATETIME)
    # Momento en el que el dato insertado en la bd. Esto permite
    # poder difereciar el momento en el que se adquirio el dato
    # con respecto al momento en el que el nodo pudo enviarlo.
    timestamp_db = db.Column(
        "timestamp_db",
        db.DATETIME,
        server_default=func.now()
    )
    volumen = db.Column("volumen", db.Float)
    temperatura = db.Column("temperatura", db.Float)
    latitud = db.Column("latitud", db.Float(precision=32))
    longitud = db.Column("longitud", db.Float(precision=32))
    # El evento le da informacion adicional al usuario frente a
    # situaciones que no son registradas directamente en alguno de
    # los datos adquiridos.
    evento = db.Column("evento", String(2))


class DatosSchema(ma.Schema):
    # Schema que permite convertir una query en un Json.

    nombre_nodo = fields.Str(attribute="nombre")
    timestamp = fields.DateTime(
        format='%d-%m-%Y %H:%M:%S',
        attribute="timestamp"
    )
    volumen = fields.Float(attribute="volumen")
    temperatura = fields.Float(attribute="temperatura")
    latitud = fields.Float(attribute="latitud")
    longitud = fields.Float(attribute="longitud")
    evento = fields.Str(attribute="evento")


datos_schema = DatosSchema(many=True)


class Nodo(db.Model):
    # Modelo de la tabla "nodo".

    __tablename__ = 'nodo'
    id = db.Column("id", db.INTEGER, primary_key=True)
    # Numero de nodo. Un usuario identifica un nodo por el
    # numero de nodo. Muchos usuarios pueden tener un "nodo 1".
    nodo = db.Column("nodo", db.INTEGER)
    # Clave foranea del cliente dueño del nodo.
    id_cliente = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    # Version de firmware del nodo. Es una de los primeros datos transmitidos
    # por el mismo.
    firmware = db.Column("firmware", String(10))
    # Momento en el que se envio la version de firmware del nodo por ultima vez
    timestamp_fm = db.Column("timestamp_fm", db.DATETIME)
    # Nombre del nodo
    nombre = db.Column("nombre", String(50))
    descripcion = db.Column("descripcion", String(100))
    datos = db.relationship("Dato", backref="nodo")


class Usuario(UserMixin, db.Model):
    # Modelo de la tabla "nodo".

    __tablename__ = 'usuario'
    id = db.Column("id", db.INTEGER, primary_key=True)
    email = db.Column("email", String(50), unique=True)
    contrasenia = db.Column("contrasenia", String(128))
    razonSocial = db.Column("razon_social", String(80))
    nodos = db.relationship("Nodo", backref="cliente")
