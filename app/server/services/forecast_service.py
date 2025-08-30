from sqlalchemy import cast, Date

from app.server import db
from app.server.models.forecast import Forecast
from app.server.models.measurement import Measurement
from app.server.models.measurement_category import MeasurementCategory
from app.server.models.measurement_unit import MeasurementUnit


class ForecastService:
    @staticmethod
    def create_forecast(city, measurement_id):
        forecast = Forecast(
            city=city,
            measurement_id=measurement_id,
        )
        db.session.add(forecast)
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
                .join(Measurement, Forecast.measurement_id == Measurement.id)
                .join(MeasurementCategory, Measurement.category_id == MeasurementCategory.id)
                .join(MeasurementUnit, Measurement.unit_id == MeasurementUnit.id)
                .filter(cast(Measurement.forecast_at, Date) == date)
        )
        return query.all()

    @staticmethod
    def delete_forecast(id):
        forecast = ForecastService.get_forecast_by_id(id)
        if forecast:
            db.session.delete(forecast)
            db.session.commit()