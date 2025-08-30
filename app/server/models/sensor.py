from app.server import db
from app.server.models.audit_model import AuditModel
from app.server.models.base_model import BaseModel


class Sensor(db.Model, BaseModel, AuditModel):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(100), unique=True, nullable=False)
    station_code = db.Column(db.String(100), db.ForeignKey('stations.code'), nullable=False)
    #measurement = db.relationship('Measurement', backref='measurements', lazy=True)