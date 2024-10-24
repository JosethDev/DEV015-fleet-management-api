import datetime
from db import db

class Taxi(db.Model):
    __tablename__ = 'taxis'
    id = db.Column(db.Integer, primary_key=True)
    # clave primaria y unica
    plate = db.Column(db.String(255), nullable=False)
    trajectories = db.relationship("Trajectory")

class Trajectory(db.Model):
    __tablename__ = 'trajectories'
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey('taxis.id'))
    # clase foranea hace referencia la tabla < taxis >
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    # por defecto la fecha actual
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # Float para datos decimales

