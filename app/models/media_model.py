from app.extension import db

class MediaModel(db.Model):
    __tablename__ = "media"

    media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)  # e.g., 'image', 'video'
    caption = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

