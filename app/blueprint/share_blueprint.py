from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.repository.share_repository import ShareRepository
from app.schema.share_schema import ShareSchema

share_blp = Blueprint('shares', 'shares', url_prefix='/shares', description="Operations for shares")

@share_blp.route("/", methods=['POST'])
@share_blp.arguments(ShareSchema)
@share_blp.response(201, ShareSchema)
@jwt_required()
def create_share(data):
    return ShareRepository.create_share(data)

@share_blp.route("/", methods=['GET'])
@share_blp.response(200, ShareSchema(many=True))
@jwt_required()
def get_all_shares():
    return ShareRepository.get_all_shares()

@share_blp.route("/<string:share_uuid>", methods=['GET'])
@share_blp.response(200, ShareSchema)
@jwt_required()
def get_share_by_uuid(share_uuid):
    share = ShareRepository.get_share_by_uuid(share_uuid)
    if not share:
        return {"message": "Share not found"}, 404
    return share

@share_blp.route("/<string:share_uuid>", methods=['PUT'])
@share_blp.arguments(ShareSchema)
@share_blp.response(200, ShareSchema)
@jwt_required()
def update_share(data, share_uuid):
    updated_share = ShareRepository.update_share(share_uuid, data)
    if not updated_share:
        return {"message": "Share not found"}, 404
    return updated_share

@share_blp.route("/<string:share_uuid>", methods=['DELETE'])
@share_blp.response(204)
@jwt_required()
def delete_share(share_uuid):
    deleted_share = ShareRepository.delete_share(share_uuid)
    if not deleted_share:
        return {"message": "Share not found"}, 404
    return ''

@share_blp.route("/user/<string:user_uuid>", methods=["GET"])
@share_blp.response(200, ShareSchema(many=True))
@jwt_required()
def get_share_by_user(user_uuid):
    user = ShareRepository.get_all_share_by_user(user_uuid)
    if user is None:
        return {"message": "User not found"}, 404
    return user


@share_blp.route("/post/<string:post_uuid>", methods=["GET"])
@share_blp.response(200, ShareSchema(many=True))
@jwt_required()
def get_share_by_user(post_uuid):
    post = ShareRepository.get_all_share_by_post(post_uuid)
    if post is None:
        return {"message": "Post not found"}, 404
    return post