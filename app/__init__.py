from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from app.api.yummy.endpoints.recipes import ns as blog_posts_namespace
from app.api.yummy.endpoints.categories import ns as blog_categories_namespace
from app.api.restplus import api
from config import config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    # config['development'].init_app(app)


    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    
    """Blue print registration"""
    ''' from .api import api as api_blueprint
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    app.register_blueprint(api_blueprint) '''
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    app.register_blueprint(blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')


    return app
