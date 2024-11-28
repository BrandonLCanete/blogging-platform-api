from os import abort

from flask import jsonify, make_response
from flask_jwt_extended import unset_jwt_cookies, jwt_required, set_access_cookies, get_jwt, get_jwt_identity
from flask_smorest import Blueprint

from app.schema.auth_schema import AuthSchema
from app.service.authentication_service import AuthenticationService

auth_blp = Blueprint('auth', 'auth', url_prefix='/auth', description="Authentication")


@auth_blp.route("/login", methods=['POST'])
@auth_blp.arguments(AuthSchema)
def login(data):
    email = data.get("email")
    password = data.get("password")

    tokens, error = AuthenticationService.authenticate_user(email, password)

    if not error is None:
        return jsonify({"message": "Invalid Credentials"}), 401

    access_token = tokens["access_token"]

    response = make_response(jsonify({"message": "Login successful"}))
    set_access_cookies(response, access_token)

    return response

@auth_blp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()

    claims = get_jwt()

    return jsonify({
        "user_id": current_user_id,
        "email": claims.get("email"),
        "role": claims.get("role")
    }), 200

@auth_blp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    unset_jwt_cookies(response)
    return response