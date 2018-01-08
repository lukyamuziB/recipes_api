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
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    jwt.init_app(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()


    """ Register api blue print and namespace"""
    
    from .api import api_v1 as api_blueprint
    from app.api.restplus import api
    from app.api.yummy.endpoints.recipes import ns as recipes_namespace
    from app.api.yummy.endpoints.categories import ns as categories_namespace
    from app.api.yummy.endpoints.user import ns as users_namespace

    api.init_app(api_blueprint)
    api.add_namespace(recipes_namespace)
    api.add_namespace(categories_namespace)
    api.add_namespace(users_namespace)
    app.register_blueprint(api_blueprint, url_prefix = '/api')
    jwt._set_error_handler_callbacks(api)


    return app
