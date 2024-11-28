from sqlalchemy.orm import joinedload

from app.models.post_model import PostModel
from app.models.share_model import ShareModel
from app.extension import db
from app.models.user_model import UserModel


class ShareRepository:
    @staticmethod
    def get_all_shares():
        return ShareModel.query.filter_by(deleted_at=None).all()

    @staticmethod
    def get_share_by_uuid(share_uuid):
        return ShareModel.query.options(
            joinedload(ShareModel.post),
            joinedload(ShareModel.user)
        ).filter_by(deleted_at=None).all()

    @staticmethod
    def get_all_share_by_user(user_uuid):
        user = UserModel.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            return None

        return ShareModel.query.filter(
            ShareModel.user_id == user.user_id,
            ShareModel.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_all_share_by_post(post_uuid):
        post = PostModel.query.filter_by(post_uuid=post_uuid).first()
        if not post:
            return None

        return ShareModel.query.filter(
            ShareModel.post_id == post.post_id,
            ShareModel.deleted_at.is_(None)
        ).all()


    @staticmethod
    def create_share(share_data):
        new_share = ShareModel(**share_data)
        db.session.add(new_share)
        db.session.commit()
        return new_share

    @staticmethod
    def update_share(share_uuid, update_data):
        share = ShareRepository.get_share_by_uuid(share_uuid)
        if not share:
            return None
        for key, value in update_data.items():
            setattr(share, key, value)
        db.session.commit()
        return share

    @staticmethod
    def delete_share(share_uuid):
        share = ShareRepository.get_share_by_uuid(share_uuid)
        if not share:
            return None
        share.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return share