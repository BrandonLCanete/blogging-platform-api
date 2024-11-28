import uuid
from sqlalchemy.dialects.mysql import CHAR
from app.extension import db

class PostModel(db.Model):
    __tablename__ = "post"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_uuid = db.Column(CHAR(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    title = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    markdown_enabled = db.Column(db.Boolean, default=False)
    draft_status = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

    comments = db.relationship("CommentModel", backref="post", lazy=True)
    media = db.relationship("MediaModel", backref="post", lazy=True)
    shares = db.relationship("ShareModel", backref="post", lazy=True)

