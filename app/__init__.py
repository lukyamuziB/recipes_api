from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api


from config import config

db = SQLAlchemy()
api = Api()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)

    api.init_app(app, version='1.0', title='Yummy Recipes',
          description='Yummy Recipes Interactive API')

    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    
    """ Register app blueprints api namespaces """


    from .api import api as api_blueprint

    """ these two imports are put here to prevent circular imports """

    from app.api.yummy.endpoints.recipes import ns as recipes_namespace
    from app.api.yummy.endpoints.categories import ns as categories_namespace

    api.add_namespace(recipes_namespace)
    api.add_namespace(categories_namespace)
    app.register_blueprint(api_blueprint, url_prefix = '/api')

    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix = '/auth')


    return app
