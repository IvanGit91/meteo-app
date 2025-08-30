from app.server import db
from app.server.models.audit_model import AuditModel
from app.server.models.base_model import BaseModel


class Forecast(db.Model, BaseModel, AuditModel):
    __tablename__ = 'forecasts'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'), nullable=False)