from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from app.server.exceptions.NotFoundException import NotFoundException
from app.server.helpers.date import is_valid_date
from app.server.services.measurement_service import MeasurementService
from app.server.models.measurement_unit import MeasurementUnit
from app.server.models.measurement_category import MeasurementCategory
from app.server.services.sensor_service import SensorService
from app.server.services.station_service import StationService
from app.server.validators.measurement_validator import MeasurementSchema

measurement_bp = Blueprint('measurement_bp', __name__)

@measurement_bp.route('/measurement', methods=['POST'])
def create_measurement():
    schema = MeasurementSchema()
    data = request.get_json()
    validated_data = schema.load(data)

    station = StationService.get_station_by_code(validated_data["sensor"])
    if station is None:
        raise NotFoundException(f'Station with code {validated_data["station_code"]} not found')

    sensor = SensorService.get_sensor_by_id(validated_data["identifier"])
    if sensor is None:
        SensorService.create_sensor(validated_data["identifier"], station.code)

    category = MeasurementService.get_or_create_measurement_category(validated_data["info"]["category"])
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["info"]["unit"])
    measurement = MeasurementService.create_measurement(
        validated_data["date"],
        category.id,
        unit.id,
        validated_data["info"]["measurement"],
        validated_data["identifier"]
    )

    return jsonify(measurement.serialize()), 200

@measurement_bp.route('/measurement-async', methods=['POST'])
def create_measurement_async():
    schema = MeasurementSchema()
    data = request.get_json()
    validated_data = schema.load(data)

    station = StationService.get_station_by_code(validated_data["sensor"])
    if station is None:
        raise NotFoundException(f'Station with code {validated_data["station_code"]} not found')

    sensor = SensorService.get_sensor_by_id(validated_data["identifier"])
    if sensor is None:
        SensorService.create_sensor(validated_data["identifier"], station.code)

    category = MeasurementService.get_or_create_measurement_category(validated_data["info"]["category"])
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["info"]["unit"])
    MeasurementService.handle_measurement_async(
        validated_data["date"],
        category.id,
        unit.id,
        validated_data["info"]["measurement"],
        validated_data["identifier"]
    )

    return jsonify({"message": "Measurement task created"}), 200

@measurement_bp.route('/measurements/<string:date_param>', methods=['GET'])
def get_measurement_by_date(date_param):
    is_valid = is_valid_date(date_param)
    if not is_valid:
        raise BadRequest("date is invalid")

    res = []
    res_by_date = MeasurementService.get_measurement_by_date_avg(date_param)
    for city, cat, unit, avg in res_by_date:
        elem = {"city": city, "cat": cat, "unit": unit, "avg": avg}
        res.append(elem)

    return jsonify(res), 200