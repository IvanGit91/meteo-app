from app.server import db
from app.server.models.audit_model import AuditModel
from app.server.models.base_model import BaseModel


class Forecast(db.Model, BaseModel, AuditModel):
    __tablename__ = 'forecasts'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), db.ForeignKey('sensors.sensor_id'), nullable=True)
    forecast_at = db.Column(db.DateTime, nullable=False)