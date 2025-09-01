from sqlalchemy import UniqueConstraint

from app.server import db
from app.server.models.audit_model import AuditModel
from app.server.models.base_model import BaseModel


class Measurement(db.Model, BaseModel, AuditModel):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    forecast_id = db.Column(db.Integer, db.ForeignKey('forecasts.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('measurement_categories.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('measurement_units.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('forecast_id', 'category_id', 'unit_id', name='uq_forecast_category_unit'),
    )