from flask import Blueprint, request, jsonify

from app.server.exceptions.NotFoundException import NotFoundException
from app.server.services.sensor_service import SensorService
from app.server.services.station_service import StationService
from app.server.validators.sensor_validator import SensorSchema

sensor_bp = Blueprint('sensor_bp', __name__)

@sensor_bp.route('/sensors', methods=['GET'])
def get_sensors():
    page = int(request.args.get('page'))
    sensors = SensorService.get_sensors(page)

    res = []
    for sensor in sensors:
        res.append(sensor.serialize())

    return jsonify(res), 200


@sensor_bp.route('/sensor', methods=['POST'])
def create_sensor():
    schema = SensorSchema()
    data = request.get_json()
    validated_data = schema.load(data)
    station = StationService.get_station_by_code(validated_data["station_code"])
    if station is None:
        raise NotFoundException(f'Station with code {validated_data["station_code"]} not found')
    sensor = SensorService.create_sensor(**validated_data)
    return jsonify(sensor.serialize()), 201


@sensor_bp.route('/sensor/<code>', methods=['DELETE'])
def delete_station(code):
    SensorService.delete_sensor(code)
    return jsonify(), 204