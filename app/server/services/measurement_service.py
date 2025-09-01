from app.server import db
from app.server.models.measurement import Measurement
from app.server.models.measurement_category import MeasurementCategory
from app.server.models.measurement_unit import MeasurementUnit
from app.server.tasks import process_measurement


class MeasurementService:
    @staticmethod
    def create_measurement(forecast_id, category_id, unit_id, value, commit=True):
        measurement = Measurement(
            forecast_id=forecast_id,
            category_id=category_id,
            unit_id=unit_id,
            value=value
        )
        db.session.add(measurement)
        if commit:
            db.session.commit()
        return measurement

    @staticmethod
    def handle_measurement_async(forecast_id, category_id, unit_id, value):
        # Process the sensor data asynchronously
        process_measurement.delay(forecast_id, category_id, unit_id, value)

    @staticmethod
    def get_or_create_measurement_category(category_name):
        category = MeasurementService.get_measurement_category_by_name(category_name)
        if category is None:
            category = MeasurementService.create_measurement_category(category_name)
        return category

    @staticmethod
    def get_or_create_measurement_unit(unit_name):
        unit = MeasurementService.get_measurement_unit_by_name(unit_name)
        if unit is None:
            unit = MeasurementService.create_measurement_unit(unit_name)
        return unit

    @staticmethod
    def create_measurement_category(name):
        measurement_cat = MeasurementCategory(name=name, display_name=name)
        db.session.add(measurement_cat)
        db.session.commit()
        return measurement_cat

    @staticmethod
    def create_measurement_unit(name):
        measurement_unit = MeasurementUnit(name=name, display_name=name)
        db.session.add(measurement_unit)
        db.session.commit()
        return measurement_unit

    @staticmethod
    def get_measurement_category_by_name(name):
        return MeasurementCategory.query.filter_by(name=name).first()

    @staticmethod
    def get_measurement_unit_by_name(name):
        return MeasurementUnit.query.filter_by(name=name).first()