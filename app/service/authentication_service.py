from flask_jwt_extended import create_access_token
from app.repository.authentication_repository import AuthenticationRepository
from app.extension import bcrypt
from app.exceptions.custom_exceptions import GenericException  # Optional for better error structure

class AuthenticationService:

    @staticmethod
    def authenticate_user(email, password):
        try:

            user = AuthenticationRepository.get_user_by_email(email)

            if not user:
                return None, "Invalid credentials"

            # Use bcrypt to verify the password
            if not bcrypt.check_password_hash(user.password, password):
                return None, "Invalid credentials"

            access_token = create_access_token(
                    identity=user.user_uuid,
                    additional_claims={"email": user.email, "role": user.user_role}
            )

            return {
                "access_token": access_token,
            }, None
        except Exception as e:
            print(e)
            raise GenericException("Authentication failed due to an unexpected error.")
