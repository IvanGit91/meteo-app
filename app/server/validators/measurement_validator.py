from marshmallow import Schema, fields, post_load


class MeasurementInfoSchema(Schema):
    category = fields.String(required=True)
    measurement = fields.Integer(required=True)
    unit = fields.String(required=True)

class MeasurementSchema(Schema):
    forecast_id = fields.Integer(required=True)
    info = fields.Nested(MeasurementInfoSchema(), required=True)

    @post_load
    def lowercase_values(self, data, **kwargs):
        data['info']["category"] = data['info']["category"].lower()
        data['info']["unit"] = data['info']["unit"].lower()
        return data