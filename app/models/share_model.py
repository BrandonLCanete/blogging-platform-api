import uuid
from sqlalchemy.dialects.mysql import CHAR
from app.extension import db

class ShareModel(db.Model):
    __tablename__ = "share"

    share_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    share_uuid = db.Column(CHAR(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)
