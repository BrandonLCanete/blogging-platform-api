from marshmallow import Schema, fields

class ShareSchema(Schema):
    share_id = fields.Int(dump_only=True)
    share_uuid = fields.Str(dump_only=True)
    post_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

    post = fields.Str(attribute="post.title", dump_only=True)
    post_uuid = fields.Str(attribute="post.post_uuid", dump_only=True)
    user = fields.Str(attribute="user.username", dump_only=True)
    user_uuid = fields.Str(attribute="user.user_uuid", dump_only=True)
    post_owner = fields.Str(attribute="post.user.username", dump_only=True)
    post_owner_uuid = fields.Str(attribute="post.user.user_uuid", dump_only=True)