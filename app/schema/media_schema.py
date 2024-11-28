from marshmallow import Schema, fields

class MediaSchema(Schema):
    media_id = fields.Int(dump_only=True)
    post_id = fields.Int(required=True)
    url = fields.Str(required=True)
    type = fields.Str(required=True)
    caption = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)