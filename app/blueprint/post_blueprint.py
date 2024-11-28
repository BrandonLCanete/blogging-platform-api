from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.repository.post_repository import PostRepository
from app.schema.post_schema import PostSchema

post_blp = Blueprint('posts', 'posts', url_prefix='/posts', description="Operations for posts")

@post_blp.route("/", methods=['POST'])
@post_blp.arguments(PostSchema)
@post_blp.response(201, PostSchema)
@jwt_required()
def create_post(data):
    return PostRepository.create_post(data)

@post_blp.route("/", methods=['GET'])
@post_blp.response(200, PostSchema(many=True))
@jwt_required()
def get_all_posts():
    return PostRepository.get_all_posts()

@post_blp.route("/<string:post_uuid>", methods=['GET'])
@post_blp.response(200, PostSchema)
@jwt_required()
def get_post_by_uuid(post_uuid):
    post = PostRepository.get_post_by_uuid(post_uuid)
    if not post:
        return {"message": "Post not found"}, 404
    return post

@post_blp.route("/<string:post_uuid>", methods=['PUT'])
@post_blp.arguments(PostSchema)
@post_blp.response(200, PostSchema)
@jwt_required()
def update_post(data, post_uuid):
    updated_post = PostRepository.update_post(post_uuid, data)
    if not updated_post:
        return {"message": "Post not found"}, 404
    return updated_post

@post_blp.route("/<string:post_uuid>", methods=['DELETE'])
@post_blp.response(204)
@jwt_required()
def delete_post(post_uuid):
    deleted_post = PostRepository.delete_post(post_uuid)
    if not deleted_post:
        return {"message": "Post not found"}, 404
    return ''

@post_blp.route("/user/<string:user_uuid>", methods=["GET"])
@post_blp.response(200, PostSchema(many=True))
@jwt_required()
def get_comments_by_user(user_uuid):
    posts = PostRepository.get_all_post_by_user(user_uuid)
    if posts is None:
        return {"message": "User not found"}, 404
    return posts

@post_blp.route("/category/<string:category_uuid>", methods=["GET"])
@post_blp.response(200, PostSchema(many=True))
@jwt_required()
def get_comments_by_user(category_uuid):
    category = PostRepository.get_all_post_by_category(category_uuid)
    if category is None:
        return {"message": "category not found"}, 404
    return category



