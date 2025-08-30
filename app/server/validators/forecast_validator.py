from marshmallow import Schema, fields, post_load


class ForecastSchema(Schema):
    sensor_id = fields.String(required=True)
    city = fields.String(required=True)
    forecast_at = fields.DateTime(required=True)
    temperature_unit = fields.String(required=True)
    temperature_value = fields.Integer(required=True, validate=lambda n: n > 0)
    humidity_unit = fields.String(required=True)
    humidity_value = fields.Integer(required=True, validate=lambda n: n > 0)
    wind_unit = fields.String(required=True)
    wind_value = fields.Integer(required=True, validate=lambda n: n > 0)

    @post_load
    def lowercase_values(self, data, **kwargs):
        data['temperature_unit'] = data['temperature_unit'].lower()
        data['humidity_unit'] = data['humidity_unit'].lower()
        data['wind_unit'] = data['wind_unit'].lower()
        return data