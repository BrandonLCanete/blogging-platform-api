from marshmallow import Schema, fields

class AuthSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, load_only=True, error_messages={"required": "Password is required."})
