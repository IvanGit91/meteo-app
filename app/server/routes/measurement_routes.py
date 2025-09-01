from flask import Blueprint, jsonify, request

from app.server.exceptions.NotFoundException import NotFoundException
from app.server.services.forecast_service import ForecastService
from app.server.services.measurement_service import MeasurementService
from app.server.validators.measurement_validator import MeasurementSchema

measurement_bp = Blueprint('measurement_bp', __name__)

@measurement_bp.route('/measurement', methods=['POST'])
def create_measurement():
    schema = MeasurementSchema()
    data = request.get_json()
    validated_data = schema.load(data)

    forecast = ForecastService.get_forecast_by_id(validated_data["forecast_id"])
    if forecast is None:
        raise NotFoundException(f'Forecast with code {validated_data["forecast_id"]} not found')

    category = MeasurementService.get_or_create_measurement_category(validated_data["info"]["category"])
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["info"]["unit"])
    measurement = MeasurementService.create_measurement(
        validated_data["forecast_id"],
        category.id,
        unit.id,
        validated_data["info"]["measurement"]
    )

    return jsonify(measurement.serialize()), 200

@measurement_bp.route('/measurement-async', methods=['POST'])
def create_measurement_async():
    schema = MeasurementSchema()
    data = request.get_json()
    validated_data = schema.load(data)

    forecast = ForecastService.get_forecast_by_id(validated_data["forecast_id"])
    if forecast is None:
        raise NotFoundException(f'Forecast with code {validated_data["forecast_id"]} not found')

    category = MeasurementService.get_or_create_measurement_category(validated_data["info"]["category"])
    unit = MeasurementService.get_or_create_measurement_unit(validated_data["info"]["unit"])
    MeasurementService.handle_measurement_async(
        validated_data["forecast_id"],
        category.id,
        unit.id,
        validated_data["info"]["measurement"]
    )

    return jsonify({"message": "Measurement task created"}), 200
