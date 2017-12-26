from flask_restplus import fields, Resource
from ..restplus import api

recipe = api.model('Recipe', {
    'id': fields.Integer(readOnly=True, description='recipe unique identifier'),
    'name': fields.String(required=True, description='recipe name'),
    'description': fields.String(required=True, description='A brief description of the recipes'),
    # 'recipe steps': fields.String(required = True, descripton = 'Procedure/ Steps of the Recipe'),
    'category_id': fields.Integer(attribute='categories.id'),
    'user_id': fields.Integer
    # 'category': fields.String(attribute='categories.name'),
})


pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

recipe_collection = api.inherit('Recipes Collection', pagination, {
    'items': fields.List(fields.Nested(recipe))})


category = api.model('Recipe Category', {
    'id': fields.Integer(readOnly=True, description='Unqiue category Id for Identity purposes'),
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required = True, description = 'A brief description of the category')
})


category_collection = api.inherit('Categories collection', pagination, {
    'items': fields.List(fields.Nested(category))
})

category_with_recipes = api.inherit('Yummy category with recipes', category, {
    'Recipe': fields.List(fields.Nested(recipe))
})


users = api.model('User', {
    'name': fields.String(required = True, description = 'Users name'),
    'username': fields.String(required = True, description = 'User unique name on the app'),
    'email':fields.String(required = True, description = 'User email'),
    'password': fields.String(required = True, description = 'user password')
})