from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from app.server import NotFoundException
from app.server.helpers.date import is_valid_date
from app.server.services.forecast_service import ForecastService
from app.server.services.measurement_service import MeasurementService
from app.server.services.sensor_service import SensorService
from app.server.validators.forecast_validator import ForecastSchema

forecast_bp = Blueprint('forecast_bp', __name__)

@forecast_bp.route('/forecast', methods=['GET'])
def get_forecasts():
    page = int(request.args.get('page'))
    forecasts = ForecastService.get_forecasts(page)

    res = []
    for forecast in forecasts:
        res.append(forecast.serialize())

    return jsonify(res), 200

@forecast_bp.route('/forecast/<string:date_param>', methods=['GET'])
def get_forecasts_by_date(date_param):
    is_valid = is_valid_date(date_param)
    if not is_valid:
        raise BadRequest("date is invalid")

    res = []
    res_by_date = ForecastService.get_forecast_by_date(date_param)
    for forecast, measurement, category, unit in res_by_date:
        forecast_serialized = forecast.serialize()
        forecast_serialized["measurement"] = measurement.serialize()
        forecast_serialized["category"] = category.name
        forecast_serialized["unit"] = unit.name
        res.append(forecast_serialized)

    return jsonify(res), 200

@forecast_bp.route('/forecast', methods=['POST'])
def create_forecast():
    schema = ForecastSchema()
    data = request.get_json()
    validated_data = schema.load(data)
    res = []

    # TODO - add sensorID to the request?

    sensor_id = validated_data["sensor_id"]
    sensor = SensorService.get_sensor_by_id(sensor_id)
    if sensor is None:
        raise NotFoundException(f'Sensor with code {sensor_id} not found')

    category = MeasurementService.get_or_create_measurement_category("temperature")
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["temperature_unit"])
    measurement = MeasurementService.create_measurement(
        validated_data["forecast_at"],
        category.id,
        unit.id,
        validated_data["temperature_value"],
        sensor_id
    )
    forecast = ForecastService.create_forecast(validated_data["city"], measurement.id)
    res.append(forecast.serialize())

    category = MeasurementService.get_or_create_measurement_category("humidity")
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["humidity_unit"])
    measurement = MeasurementService.create_measurement(
        validated_data["forecast_at"],
        category.id,
        unit.id,
        validated_data["humidity_value"],
        sensor_id
    )
    forecast = ForecastService.create_forecast(validated_data["city"], measurement.id)
    res.append(forecast.serialize())

    category = MeasurementService.get_or_create_measurement_category("wind")
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["wind_unit"])
    measurement = MeasurementService.create_measurement(
        validated_data["forecast_at"],
        category.id,
        unit.id,
        validated_data["wind_value"],
        sensor_id
    )
    # TODO - city probably is not needed
    # TODO - probably the forecast table is not needed either
    forecast = ForecastService.create_forecast(validated_data["city"], measurement.id)
    res.append(forecast.serialize())
    return jsonify(res), 200


@forecast_bp.route('/forecast/<code>', methods=['DELETE'])
def delete_station(code):
    ForecastService.delete_forecast(code)
    return jsonify(), 204