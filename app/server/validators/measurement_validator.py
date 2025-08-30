from marshmallow import Schema, fields, post_load


class MeasurementInfoSchema(Schema):
    category = fields.String(required=True)
    measurement = fields.Integer(required=True)
    unit = fields.String(required=True)

class MeasurementSchema(Schema):
    identifier = fields.String(required=True)
    sensor = fields.String(required=True)
    city = fields.String(required=True)
    date = fields.DateTime(required=True)
    info = fields.Nested(MeasurementInfoSchema(), required=True)

    @post_load
    def lowercase_values(self, data, **kwargs):
        data['info']["category"] = data['info']["category"].lower()
        data['info']["unit"] = data['info']["unit"].lower()
        return data