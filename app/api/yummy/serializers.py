from flask_restplus import fields, Resource
from ..restplus import api


""" this file is for data validation """

recipe = api.model('Recipe', {
    'id': fields.Integer(readOnly=True, description='recipe unique identifier'),
    'name': fields.String(required=True, description='recipe name'),
    'description': fields.String(required=True, description='A brief description of the recipes'),
    'created': fields.DateTime(readOnly=True, description = 'Date created'),
    'modified': fields.DateTime(readOnnly=True, description = 'date modified'),
    'category_id': fields.Integer(readOnly = True, description = 'category recipe belongs to'),
    'user_id': fields.Integer(readOnly = True, description = 'User that made recipe')
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
    'description': fields.String(required = True, description = 'A brief description of the category'),
    'created': fields.DateTime(readOnly=True, description = 'Date created'),
    'modified': fields.DateTime(readOnnly=True, description = 'date modified'),
    'user_id': fields.Integer(readOnly = True, description='User that made the category')
})


category_collection = api.inherit('Categories collection', pagination, {
    'items': fields.List(fields.Nested(category))
})

category_with_recipes = api.inherit('Yummy category with recipes', category, {
    'Recipe': fields.List(fields.Nested(recipe))
})


users = api.model('User', {
    'name': fields.String(required = True, description = 'Users name'),
    'username': fields.String(required = True,
       pattern = '^[a-z]+$', description = 'User unique name on the app'),
    'email':fields.String(required = True, description = 'User email'),
    'password': fields.String(required = True, description = 'user password')
})


usr = api.model('user log in', {
    'username': fields.String(required = True, description = 'User unique name on the app'),
    'password':fields.String(required = True, description = 'User email')
  
})

username_reset = api.model('Reset user username', {
    'username': fields.String(required = True, description = 'User username')
})

users_password_reset = api.model('Reset Password', {
    'password': fields.String(required = True, description = 'User Password')
})