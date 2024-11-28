from app.models.media_model import MediaModel
from app.extension import db

class MediaRepository:
    @staticmethod
    def get_all_media():
        return MediaModel.query.filter_by(deleted_at=None).all()

    @staticmethod
    def get_media_by_id(media_id):
        return MediaModel.query.filter_by(media_id=media_id, deleted_at=None).first()

    @staticmethod
    def create_media(media_data):
        new_media = MediaModel(**media_data)
        db.session.add(new_media)
        db.session.commit()
        return new_media

    @staticmethod
    def update_media(media_id, update_data):
        media = MediaRepository.get_media_by_id(media_id)
        if not media:
            return None
        for key, value in update_data.items():
            setattr(media, key, value)
        db.session.commit()
        return media

    @staticmethod
    def delete_media(media_id):
        media = MediaRepository.get_media_by_id(media_id)
        if not media:
            return None
        media.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return media
