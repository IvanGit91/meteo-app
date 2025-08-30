from sqlalchemy import cast, Date, func
from app.server import db
from app.server.models.measurement import Measurement
from app.server.models.sensor import Sensor
from app.server.models.station import Station
from app.server.tasks import process_measurement
from app.server.models.measurement_unit import MeasurementUnit
from app.server.models.measurement_category import MeasurementCategory

class MeasurementService:
    @staticmethod
    def create_measurement(forecast_at, category_id, unit_id, value, sensor_id = None):
        measurement = Measurement(
            forecast_at=forecast_at,
            category_id=category_id,
            unit_id=unit_id,
            value=value,
            sensor_id=sensor_id,
        )
        db.session.add(measurement)
        db.session.commit()
        return measurement

    @staticmethod
    def handle_measurement_async(forecast_at, category_id, unit_id, value, sensor_id):
        # Process the sensor data asynchronously
        process_measurement.delay(forecast_at, category_id, unit_id, value, sensor_id)

    @staticmethod
    def get_measurement_by_date(date):
        query = (
            db.session.query(Measurement, MeasurementUnit, MeasurementCategory)
                .join(MeasurementCategory, Measurement.category_id == MeasurementCategory.id)
                .join(MeasurementUnit, Measurement.unit_id == MeasurementUnit.id)
                .filter(cast(Measurement.forecast_at, Date) == date)
        )
        return query.all()

    @staticmethod
    def get_measurement_by_date_avg(date):
        query = (
            db.session.query(Station.city, MeasurementUnit.name, MeasurementCategory.name, func.avg(Measurement.value).label('average_amount'))
                .join(MeasurementCategory, Measurement.category_id == MeasurementCategory.id)
                .join(MeasurementUnit, Measurement.unit_id == MeasurementUnit.id)
                .join(Sensor, Measurement.sensor_id == Sensor.sensor_id)
                .join(Station, Sensor.station_code == Station.code)
                .filter(cast(Measurement.forecast_at, Date) == date)
                .group_by(Station.city, MeasurementUnit.name, MeasurementCategory.name)
        )
        return query.all()

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