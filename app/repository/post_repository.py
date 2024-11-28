from sqlalchemy.orm import joinedload

from app.models.category_model import CategoryModel
from app.models.post_model import PostModel
from app.extension import db
from app.models.user_model import UserModel


class PostRepository:
    @staticmethod
    def get_all_posts():
        return PostModel.query.options(
            joinedload(PostModel.category),
            joinedload(PostModel.user)
        ).filter(PostModel.deleted_at.is_(None)).all()

    @staticmethod
    def get_post_by_uuid(post_uuid):
        return PostModel.query.filter_by(post_uuid=post_uuid, deleted_at=None).first()

    @staticmethod
    def create_post(post_data):
        new_post = PostModel(**post_data)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def update_post(post_uuid, update_data):
        post = PostRepository.get_post_by_uuid(post_uuid)
        if not post:
            return None
        for key, value in update_data.items():
            setattr(post, key, value)
        db.session.commit()
        return post

    @staticmethod
    def get_all_post_by_user(user_uuid):
        user = UserModel.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            return None

        return PostModel.query.options(
            joinedload(PostModel.user)
        ).filter(
            PostModel.user_id == user.user_id,
            PostModel.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_all_post_by_category(category_uuid):
        category = CategoryModel.query.filter_by(category_uuid=category_uuid).first()
        if not category:
            return None

        return PostModel.query.options(
            joinedload(PostModel.user)
        ).filter(
            PostModel.category_id == category.category_id,
            PostModel.deleted_at.is_(None)
        ).all()

    @staticmethod
    def delete_post(post_uuid):
        post = PostRepository.get_post_by_uuid(post_uuid)
        if not post:
            return None
        post.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return post
