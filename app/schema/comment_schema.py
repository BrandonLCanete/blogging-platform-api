from marshmallow import Schema, fields

class CommentSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    comment_uuid = fields.Str(dump_only=True)
    post_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)
    approved = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    post = fields.Nested(
        "PostSchema",
        only=("title", "user_id"),
        dump_only=True
    )
    user = fields.Nested(
        "UserSchema",
        only=("user_id", "username"),
        dump_only=True
    )

    post = fields.Str(attribute="post.title", dump_only=True)
    user = fields.Str(attribute="user.username", dump_only=True)
    user_uuid = fields.Str(attribute="user.user_uuid", dump_only=True)
    post_owner = fields.Str(attribute="post.user.username", dump_only=True)
    post_uuid = fields.Str(attribute="post.user.post_uuid", dump_only=True)

