from app.server import db
from app.server.models.audit_model import AuditModel
from app.server.models.base_model import BaseModel


class MeasurementCategory(db.Model, BaseModel, AuditModel):
    __tablename__ = 'measurement_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
