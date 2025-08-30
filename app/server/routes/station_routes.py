from flask import Blueprint, jsonify, request
from app.server.services.station_service import StationService
from app.server.validators.station_validator import StationSchema

station_bp = Blueprint('station_bp', __name__)

@station_bp.route('/stations', methods=['GET'])
def get_station():
    page = int(request.args.get('page'))
    stations = StationService.get_stations(page)

    ss = []
    for station in stations:
        ss.append(station.serialize())

    return jsonify(ss), 200

@station_bp.route('/station/<id>', methods=['GET'])
def get_station_by_id(id):
    station = StationService.get_station_by_id(id)
    station = station.serialize() if station else {}
    return jsonify(station), 200

@station_bp.route('/station', methods=['POST'])
def create_station():
    schema = StationSchema()
    data = request.get_json()
    validated_data = schema.load(data)
    # TODO - check for duplicate station
    station = StationService.create_station(**validated_data)
    return jsonify(station.serialize()), 201

@station_bp.route('/station/<code>', methods=['DELETE'])
def delete_station(code):
    StationService.delete_station(code)
    return jsonify(), 204
