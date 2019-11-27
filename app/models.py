from . import db, ma
from sqlalchemy import Table, Column, Float, Integer, String, ForeignKey, func
from flask_login import UserMixin
from datetime import datetime
from marshmallow import fields


class Dato(db.Model):
    __tablename__ = 'dato'
    id = db.Column("id", db.Integer, primary_key=True)
    id_nodo = db.Column(db.Integer, db.ForeignKey("nodo.id"))
    timestamp = db.Column("timestamp", db.DATETIME)
    timestamp_db = db.Column(
        "timestamp_db",
        db.DATETIME,
        server_default=func.now()
    )
    volumen = db.Column("volumen", db.Float)
    temperatura = db.Column("temperatura", db.Float)
    latitud = db.Column("latitud", db.Float(precision=32))
    longitud = db.Column("longitud", db.Float(precision=32))
    evento = db.Column("evento", String(2))


class DatosSchema(ma.Schema):
    nombre_nodo = fields.Str(attribute="nombre")
    timestamp = fields.DateTime(format='%d-%m-%Y %H:%M:%S', attribute="timestamp")
    volumen = fields.Float(attribute="volumen")
    temperatura = fields.Float(attribute="temperatura")
    latitud = fields.Float(attribute="latitud")
    longitud = fields.Float(attribute="longitud")
    evento = fields.Str(attribute="evento")


datos_schema = DatosSchema(many=True)


class Nodo(db.Model):
    __tablename__ = 'nodo'
    id = db.Column("id", db.INTEGER, primary_key=True)
    nodo = db.Column("nodo", db.INTEGER)
    id_cliente = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    firmware = db.Column("firmware", String(10))
    timestamp_fm = db.Column("timestamp_fm",db.DATETIME)
    nombre = db.Column("nombre", String(50))
    descripcion = db.Column("descripcion", String(100))
    datos = db.relationship("Dato", backref="nodo")


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column("id", db.INTEGER, primary_key=True)
    email = db.Column("email", String(50), unique=True)
    contrasenia = db.Column("contrasenia", String(128))
    razonSocial = db.Column("razon_social", String(80))
    nodos = db.relationship("Nodo", backref="cliente")
