from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.repository.comment_repository import CommentRepository
from app.schema.comment_schema import CommentSchema
from app.utils.auth_utils import role_required, is_owner_or_admin

comment_blp = Blueprint('comments', 'comments', url_prefix='/comments', description="Operations for comments")

@comment_blp.route("/", methods=['POST'])
@comment_blp.arguments(CommentSchema)
@comment_blp.response(201, CommentSchema)
@jwt_required()
def create_comment(data):
    return CommentRepository.create_comment(data)

@comment_blp.route("/", methods=['GET'])
@comment_blp.response(200, CommentSchema(many=True))
@jwt_required()
def get_all_comments():
    return CommentRepository.get_all_comments()

@comment_blp.route("/<string:comment_uuid>", methods=['GET'])
@comment_blp.response(200, CommentSchema)
@jwt_required()
def get_comment_by_uuid(comment_uuid):
    comment = CommentRepository.get_comment_by_uuid(comment_uuid)
    if not comment:
        return {"message": "Comment not found"}, 404
    return comment

@comment_blp.route("/<string:comment_uuid>", methods=['PUT'])
@comment_blp.arguments(CommentSchema)
@comment_blp.response(200, CommentSchema)
@jwt_required()
@is_owner_or_admin(lambda comment_uuid: CommentRepository.get_comment_by_uuid(comment_uuid))
def update_comment(data, comment_uuid):
    updated_comment = CommentRepository.update_comment(comment_uuid, data)
    if not updated_comment:
        return {"message": "Comment not found"}, 404
    return updated_comment

@comment_blp.route("/<string:comment_uuid>", methods=['DELETE'])
@comment_blp.response(204)
@jwt_required()
def delete_comment(comment_uuid):
    deleted_comment = CommentRepository.delete_comment(comment_uuid)
    if not deleted_comment:
        return {"message": "Comment not found"}, 404
    return ''

@comment_blp.route("/post/<string:post_uuid>", methods=["GET"])
@comment_blp.response(200, CommentSchema(many=True))
@jwt_required()
def get_comments_by_post(post_uuid):
    comments = CommentRepository.get_all_comments_by_post(post_uuid)
    if comments is None:
        return {"message": "Post not found"}, 404
    return comments

@comment_blp.route("/user/<string:user_uuid>", methods=["GET"])
@comment_blp.response(200, CommentSchema(many=True))
@jwt_required()
def get_comments_by_user(user_uuid):
    comments = CommentRepository.get_all_comments_by_user(user_uuid)
    if comments is None:
        return {"message": "User not found"}, 404
    return comments
