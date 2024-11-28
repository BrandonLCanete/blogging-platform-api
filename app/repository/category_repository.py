from app.models.category_model import CategoryModel
from app.extension import db

class CategoryRepository:
    @staticmethod
    def get_all_categories():
        return CategoryModel.query.filter_by(deleted_at=None).all()

    @staticmethod
    def get_category_by_uuid(category_uuid):
        return CategoryModel.query.filter_by(category_uuid=category_uuid, deleted_at=None).first()

    @staticmethod
    def create_category(category_data):
        new_category = CategoryModel(**category_data)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def update_category(category_uuid, update_data):
        category = CategoryRepository.get_category_by_uuid(category_uuid)
        if not category:
            return None
        for key, value in update_data.items():
            setattr(category, key, value)
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category_uuid):
        category = CategoryRepository.get_category_by_uuid(category_uuid)
        if not category:
            return None
        category.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return category
