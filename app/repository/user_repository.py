import logging

from flask import jsonify

from app.models.user_model import UserModel
from app.extension import db, bcrypt

logger = logging.getLogger(__name__)

class UserRepository:
    @staticmethod
    def get_all_users():
        return UserModel.query.filter_by(deleted_at=None).all()

    @staticmethod
    def get_user_by_uuid(user_uuid):
        return UserModel.query.filter_by(user_uuid=user_uuid, deleted_at=None).first()

    @staticmethod
    def create_user(user_data):
        user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode("utf-8")
        new_user = UserModel(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_uuid, update_data):
        user = UserRepository.get_user_by_uuid(user_uuid)
        if not user:
            return jsonify({"message": "user not found"}), 404
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_uuid):
        user = UserRepository.get_user_by_uuid(user_uuid)
        if not user:
            return jsonify({"message": "user not found"}) , 404
        user.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return ''
