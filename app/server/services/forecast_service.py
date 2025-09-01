from sqlalchemy import cast, Date, func

from app.server import db
from app.server.models.forecast import Forecast
from app.server.models.measurement import Measurement
from app.server.models.measurement_category import MeasurementCategory
from app.server.models.measurement_unit import MeasurementUnit
from app.server.models.sensor import Sensor
from app.server.models.station import Station


class ForecastService:
    @staticmethod
    def create_forecast(sensor_id, forecast_at, commit=True):
        forecast = Forecast(
            sensor_id=sensor_id,
            forecast_at=forecast_at,
        )
        db.session.add(forecast)
        if commit:
            db.session.commit()
        return forecast

    @staticmethod
    def get_forecasts(page):
        return db.paginate(Forecast.query, page=page, per_page=10, error_out=False).items

    @staticmethod
    def get_forecast_by_id(id):
        return Forecast.query.filter_by(id=id).first()

    @staticmethod
    def get_forecast_by_date(date):
        query = (
            db.session.query(Forecast, Measurement, MeasurementUnit, MeasurementCategory)
                .join(Measurement, Forecast.id == Measurement.forecast_id)
                .join(MeasurementCategory, Measurement.category_id == MeasurementCategory.id)
                .join(MeasurementUnit, Measurement.unit_id == MeasurementUnit.id)
                .filter(cast(Forecast.forecast_at, Date) == date)
        )
        return query.all()

    @staticmethod
    def get_forecast_by_date_avg(date):
        query = (
            db.session.query(Station.city, MeasurementUnit.name, MeasurementCategory.name, func.avg(Measurement.value).label('average_amount'))
                .join(Measurement, Forecast.id == Measurement.forecast_id)
                .join(MeasurementCategory, Measurement.category_id == MeasurementCategory.id)
                .join(MeasurementUnit, Measurement.unit_id == MeasurementUnit.id)
                .join(Sensor, Forecast.sensor_id == Sensor.sensor_id)
                .join(Station, Sensor.station_code == Station.code)
                .filter(cast(Forecast.forecast_at, Date) == date)
                .group_by(Station.city, MeasurementUnit.name, MeasurementCategory.name)
        )
        return query.all()

    @staticmethod
    def delete_forecast(id):
        forecast = ForecastService.get_forecast_by_id(id)
        if forecast:
            db.session.delete(forecast)
            db.session.commit()