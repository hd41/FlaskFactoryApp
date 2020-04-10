from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    # TESTING = environ.get('TESTING')
    # FLASK_DEBUG = environ.get('FLASK_DEBUG')
    # SECRET_KEY = environ.get('SECRET_KEY')
    TESTING = True
    FLASK_DEBUG = False
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

    # Database
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:tiger@localhost/db_name'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:tiger@localhost:3306/covid19'
    SQLALCHEMY_DB_SCHEMA = 'public'
    SQLALCHEMY_TRACK_MODIFICATIONS = False