from flask_jwt_extended import get_jwt_identity, get_jwt
from functools import wraps
from flask import abort

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                abort(403, description="Access forbidden: insufficient privileges")
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def is_owner_or_admin(resolve_entity):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            current_user_uuid = get_jwt_identity()

            entity = resolve_entity(**kwargs)
            if not entity:
                abort(404, description="Entity not found.")

            if claims.get("role") == "ADMIN" or current_user_uuid == entity.user.user_uuid:
                return fn(*args, **kwargs)
            abort(403, description="Access forbidden: unauthorized user.")
        return decorator
    return wrapper
