from sqlalchemy.orm import joinedload

from app.models.comment_model import CommentModel
from app.extension import db
from app.models.post_model import PostModel
from app.models.user_model import UserModel


class CommentRepository:
    @staticmethod
    def get_all_comments():
        return CommentModel.query.options(
            joinedload(CommentModel.post),
            joinedload(CommentModel.user)
        ).filter_by(deleted_at=None).all()

    @staticmethod
    def get_comment_by_uuid(comment_uuid):
        return CommentModel.query.filter_by(comment_uuid=comment_uuid, deleted_at=None).first()

    @staticmethod
    def get_all_comments_by_post(post_uuid):
        return CommentModel.query.options(
            joinedload(CommentModel.user)
        ).filter(
            CommentModel.post_uuid == post_uuid,
            CommentModel.deleted_at == None
        ).all()

    @staticmethod
    def create_comment(comment_data):
        new_comment = CommentModel(**comment_data)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def get_all_comments_by_post(post_uuid):
        post = PostModel.query.filter_by(post_uuid=post_uuid).first()
        if not post:
            return None

        return CommentModel.query.options(
            joinedload(CommentModel.user)
        ).filter(
            CommentModel.post_id == post.post_id,
            CommentModel.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_all_comments_by_user(user_uuid):
        user = UserModel.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            return None

        return CommentModel.query.options(
            joinedload(CommentModel.post)
        ).filter(
            CommentModel.user_id == user.user_id,
            CommentModel.deleted_at.is_(None)
        ).all()

    @staticmethod
    def update_comment(comment_uuid, update_data):
        comment = CommentRepository.get_comment_by_uuid(comment_uuid)
        if not comment:
            return None
        for key, value in update_data.items():
            setattr(comment, key, value)
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment_uuid):
        comment = CommentRepository.get_comment_by_uuid(comment_uuid)
        if not comment:
            return None
        comment.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return comment
