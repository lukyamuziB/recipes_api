from flask_restplus import fields, Resource
from ..restplus import api

recipe = api.model('Recipe', {
    'id': fields.Integer(readOnly=True, description='recipe unique identifier'),
    'name': fields.String(required=True, description='recipe name'),
    'description': fields.String(required=True, description='A brief description of the recipes'),
    'recipe steps': fields.String(required = True, descripton = 'Procedure/ Steps of the Recipe'),
    'category_id': fields.Integer(attribute='category.id'),
    'category': fields.String(attribute='category.id'),
})

recipe_collection = api.inherit('Recipes Collection', recipe, {
    'items': fields.List(fields.Nested(recipe))})

category = api.model('Recipe Category', {
    'id': fields.Integer(readOnly=True, description='Unqiue category Id for Identity purposes'),
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required = True, description = 'A brief description of the category')
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