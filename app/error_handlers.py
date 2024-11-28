import re

from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError, DataError
from app.exceptions.custom_exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException,
    GenericException
)

def register_error_handlers(app):
    @app.errorhandler(ValidationException)
    def handle_validation_exception(error):
        response = jsonify({"error": error.message})
        response.status_code = 400
        return response

    @app.errorhandler(NotFoundException)
    def handle_not_found_exception(error):
        response = jsonify({"error": error.message})
        response.status_code = 404
        return response

    @app.errorhandler(ConflictException)
    def handle_conflict_exception(error):
        response = jsonify({"error": error.message})
        response.status_code = 409
        return response

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Handles database IntegrityError (e.g., duplicate entries, foreign key violations)."""
        details = str(error.orig)

        # Patterns for duplicate entry and foreign key violations
        duplicate_pattern = r"for key '(.+?)'"
        foreign_key_pattern = r"FOREIGN KEY \(`(.+?)`\) REFERENCES `(.+?)` \(`(.+?)`\)"

        # Match duplicate entry errors
        duplicate_match = re.search(duplicate_pattern, details)
        # Match foreign key constraint violations
        foreign_key_match = re.search(foreign_key_pattern, details)

        if duplicate_match:
            field_name = duplicate_match.group(1)
            response = jsonify({"error": f"Conflict: Duplicate entry for '{field_name}' field."})
        elif foreign_key_match:
            violated_field = foreign_key_match.group(1)
            referenced_table = foreign_key_match.group(2)
            referenced_field = foreign_key_match.group(3)
            response = jsonify({
                "error": f"Foreign key constraint failed. '{violated_field}' must reference an existing value in '{referenced_table}.{referenced_field}'."
            })
        else:
            response = jsonify({"error": "Conflict occurred in database operation."})

        print(f"IntegrityError Details: {details}")

        response.status_code = 409
        return response

    @app.errorhandler(DataError)
    def handle_data_error(error):
        """Handles invalid ENUM or data constraints."""
        details = str(error.orig)

        field_pattern = r"for column '(.+?)'"
        match = re.search(field_pattern, details)

        if match:
            field_name = match.group(1)
            response = jsonify({"error": f"Invalid value for '{field_name}'"})
        else:
            response = jsonify({"error": "Invalid data provided."})

        response.status_code = 400
        return response

    @app.errorhandler(GenericException)
    def handle_generic_exception(error):
        response = jsonify({"error": error.message})
        response.status_code = 500
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        response = jsonify({
            "error": "An unexpected error occurred",
            "details": str(error)
        })
        response.status_code = 500
        print(error)
        return response

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token_error(error):
        """Handles expired tokens."""
        response = jsonify({"error": "Token has expired"})
        response.status_code = 401
        return response

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token_error(error):
        """Handles invalid tokens."""
        response = jsonify({"error": "Invalid token provided"})
        response.status_code = 401
        return response

    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(error):
        """Handles missing or invalid authorization headers."""
        response = jsonify({"error": "Authorization token is missing or invalid"})
        response.status_code = 401
        return response