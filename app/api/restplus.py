from app import jwt
from flask_restplus import Api
from . import api_v1 as api_blueprint

api = Api(api_blueprint, version='1.0', title='Yummy Recipes',
          description='Yummy Recipes Interactive API')

from app.api.yummy.endpoints.recipes import ns as recipes_namespace
from app.api.yummy.endpoints.categories import ns as categories_namespace
from app.api.yummy.endpoints.user import ns as users_namespace    

api.add_namespace(recipes_namespace)
api.add_namespace(categories_namespace)
api.add_namespace(users_namespace)   

jwt._set_error_handler_callbacks(api) 

