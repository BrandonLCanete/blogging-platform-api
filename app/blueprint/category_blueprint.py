from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.repository.category_repository import CategoryRepository
from app.schema.category_schema import CategorySchema

category_blp = Blueprint('categories', 'categories', url_prefix='/categories', description="Operations for categories")

@category_blp.route("/", methods=['POST'])
@category_blp.arguments(CategorySchema)
@category_blp.response(201, CategorySchema)
@jwt_required()
def create_category(data):
    return CategoryRepository.create_category(data)

@category_blp.route("/", methods=['GET'])
@category_blp.response(200, CategorySchema(many=True))
@jwt_required()
def get_all_categories():
    return CategoryRepository.get_all_categories()

@category_blp.route("/<string:category_uuid>", methods=['GET'])
@category_blp.response(200, CategorySchema)
@jwt_required()
def get_category_by_uuid(category_uuid):
    category = CategoryRepository.get_category_by_uuid(category_uuid)
    if not category:
        return {"message": "Category not found"}, 404
    return category

@category_blp.route("/<string:category_uuid>", methods=['PUT'])
@category_blp.arguments(CategorySchema)
@category_blp.response(200, CategorySchema)
@jwt_required()
def update_category(data, category_uuid):
    updated_category = CategoryRepository.update_category(category_uuid, data)
    if not updated_category:
        return {"message": "Category not found"}, 404
    return updated_category

@category_blp.route("/<string:category_uuid>", methods=['DELETE'])
@category_blp.response(204)
@jwt_required()
def delete_category(category_uuid):
    deleted_category = CategoryRepository.delete_category(category_uuid)
    if not deleted_category:
        return {"message": "Category not found"}, 404
    return ''