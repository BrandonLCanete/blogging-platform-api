from flask import Flask, jsonify
from flask_smorest import Api

from app.blueprint.authentication_blueprint import auth_blp
from app.blueprint.category_blueprint import category_blp
from app.blueprint.comment_blueprint import comment_blp
from app.blueprint.media_blueprint import media_blp
from app.blueprint.post_blueprint import post_blp
from app.blueprint.share_blueprint import share_blp
from app.blueprint.user_blueprint import user_blp
from app.error_handlers import register_error_handlers
from app.extension import db, migrate, bcrypt, jwt
from config import Config
from app.models import user_model, category_model, comment_model, media_model, post_model, share_model


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    api.register_blueprint(user_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(comment_blp)
    api.register_blueprint(post_blp)
    api.register_blueprint(media_blp)
    api.register_blueprint(share_blp)
    api.register_blueprint(category_blp)


    register_error_handlers(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Hello World"})

    return app