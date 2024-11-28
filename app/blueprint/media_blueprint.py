from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.repository.media_repository import MediaRepository
from app.schema.media_schema import MediaSchema

media_blp = Blueprint('media', 'media', url_prefix='/media', description="Operations for media")

@media_blp.route("/", methods=['POST'])
@media_blp.arguments(MediaSchema)
@media_blp.response(201, MediaSchema)
@jwt_required()
def create_media(data):
    return MediaRepository.create_media(data)

@media_blp.route("/", methods=['GET'])
@media_blp.response(200, MediaSchema(many=True))
@jwt_required()
def get_all_media():
    return MediaRepository.get_all_media()

@media_blp.route("/<string:media_id>", methods=['GET'])
@media_blp.response(200, MediaSchema)
@jwt_required()
def get_media_by_uuid(media_id):
    media = MediaRepository.get_media_by_id(media_id)
    if not media:
        return {"message": "Media not found"}, 404
    return media

@media_blp.route("/<string:media_uuid>", methods=['PUT'])
@media_blp.arguments(MediaSchema)
@media_blp.response(200, MediaSchema)
@jwt_required()
def update_media(data, media_uuid):
    updated_media = MediaRepository.update_media(media_uuid, data)
    if not updated_media:
        return {"message": "Media not found"}, 404
    return updated_media

@media_blp.route("/<string:media_uuid>", methods=['DELETE'])
@media_blp.response(204)
@jwt_required()
def delete_media(media_uuid):
    deleted_media = MediaRepository.delete_media(media_uuid)
    if not deleted_media:
        return {"message": "Media not found"}, 404
    return ''
