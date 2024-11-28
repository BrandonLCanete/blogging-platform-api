from marshmallow import Schema, fields

class PostSchema(Schema):
    post_id = fields.Int(dump_only=True)
    post_uuid = fields.Str(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    markdown_enabled = fields.Bool()
    draft_status = fields.Bool()
    visibility = fields.Bool()
    scheduled_at = fields.DateTime()
    date_posted = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # category = fields.Nested(
    #     "CategorySchema",
    #     only=("name"),
    #     dump_only=True
    # )

    category = fields.Str(attribute="category.name", dump_only=True)
    category_uuid = fields.Str(attribute="category.category_uuid", dump_only=True)
    user = fields.Str(attribute="user.username", dump_only=True)
    user_uuid = fields.Str(attribute="user.user_uuid", dump_only=True)
