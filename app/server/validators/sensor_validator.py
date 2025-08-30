from marshmallow import Schema, fields

class SensorSchema(Schema):
    sensor_id = fields.String(required=True)
    station_code = fields.String(required=True)