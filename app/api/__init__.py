from flask import Blueprint

api = Blueprint('api', __name__)


from app.api.yummy.endpoints import recipes, categories
from . import restplus
from app.api.yummy import utilities, serializers, parsers
from app.api.yummy.endpoints.recipes import ns as blog_posts_namespace
from app.api.yummy.endpoints.categories import ns as blog_categories_namespace
