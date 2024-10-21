import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Taxi(db.Model):
    __tablename__ = 'taxis'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(255), nullable=False)
    trajectories = db.relationship("Trajectory")

class Trajectory(db.Model):
    __tablename__ = 'trajectories'
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey('taxis.id'))
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

