import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_TITLE = "RESTAURANT API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 15)))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    if FLASK_ENV == 'production':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_PRODUCTION')
        SQLALCHEMY_ENGINE_OPTIONS = {}  # No SSL in production (or customize as needed)
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_DEVELOPMENT')
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'ssl': {
                    'ca': os.path.join(os.getcwd(), 'app/certs/ca.pem')
                }
            }
        }
