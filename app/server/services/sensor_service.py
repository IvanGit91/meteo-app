from app.server import db
from app.server.models.sensor import Sensor
class SensorService:
    @staticmethod
    def create_sensor(sensor_id, station_code):
        sensor = Sensor(
            sensor_id=sensor_id,
            station_code=station_code
        )
        db.session.add(sensor)
        db.session.commit()
        return sensor

    @staticmethod
    def get_sensors(page):
        return db.paginate(Sensor.query, page=page, per_page=10, error_out=False).items

    @staticmethod
    def get_sensor_by_id(sensor_id):
        return Sensor.query.filter_by(sensor_id=sensor_id).first()

    @staticmethod
    def delete_sensor(sensor_id):
        sensor = SensorService.get_sensor_by_id(sensor_id)
        if sensor:
            db.session.delete(sensor)
            db.session.commit()