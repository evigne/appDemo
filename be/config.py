import os
from flask_cors import CORS
from models import db
from flask import Flask

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI ='postgresql://vigneshwarane:vignesh@localhost/spacecraft'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def get_db_config():
    if os.environ.get('ENV') == 'TEST':
        return TestConfig
    else:
        return Config


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app)
    flask_app.config.from_object(get_db_config())
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
    return flask_app
