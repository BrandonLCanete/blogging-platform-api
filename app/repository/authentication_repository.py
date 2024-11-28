from app.models.user_model import UserModel

class AuthenticationRepository:

    @staticmethod
    def get_user_by_email(email):
        return UserModel.query.filter_by(email=email, deleted_at=None).first()