
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_jwt_extended import (
    JWTManager, jwt_manager, jwt_required, create_access_token
)


db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt.init_app(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    """ Register api blue print"""
    
    from .api import api_v1 as api_blueprint
    from app.api.restplus import api
    app.register_blueprint(api_blueprint, url_prefix = '/api')

      
    return app
