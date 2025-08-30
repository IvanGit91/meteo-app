from marshmallow import Schema, fields

class StationSchema(Schema):
    code = fields.String(required=True)
    city = fields.String(required=True)
    latitude = fields.Float(required=True, validate=lambda n: n > 0)
    longitude = fields.Float(required=True, validate=lambda n: n > 0)
    installed_at = fields.Date(required=True)