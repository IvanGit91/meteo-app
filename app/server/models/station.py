from dataclasses import dataclass

from app.server import db
from app.server.models.audit_model import AuditModel
from app.server.models.base_model import BaseModel

@dataclass
class Station(db.Model, BaseModel, AuditModel):
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    installed_at = db.Column(db.Date, nullable=False)
    #sensors = db.relationship('Sensor', backref='stations', lazy=True)