from marshmallow import Schema, fields

class CategorySchema(Schema):
    category_id = fields.Int(dump_only=True)
    category_uuid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
