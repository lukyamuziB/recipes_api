from flask_restplus import fields, Resource
from ..restplus import api


""" this file is for data validation """

recipes = api.model('Recipe', {
    'id': fields.Integer(readOnly=True, description='recipe unique identifier'),
    'name': fields.String(required=True, description='recipe name'),
    'description': fields.String(required=True, description='A brief description of the recipes'),
    'created': fields.DateTime(readOnly=True, description = 'Date created'),
    'modified': fields.DateTime(readOnnly=True, description = 'date modified'),
    'category_id': fields.Integer(readOnly = True, description = 'category recipe belongs to'),
    'user_id': fields.Integer(readOnly = True, description = 'User that made recipe')
})

edit_recipe = api.model('Edit Recipe',{
    'name': fields.String(required=False, description='Category name'),
    'description': fields.String(required = False, description = 'A brief description of the category')
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

recipe_collection = api.inherit('Recipes Collection', pagination, {
    'items': fields.List(fields.Nested(recipes))})


category = api.model('Recipe Category', {
    'id': fields.Integer(readOnly=True, description='Unqiue category Id for Identity purposes'),
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required = True, description = 'A brief description of the category'),
    'created': fields.DateTime(readOnly=True, description = 'Date created'),
    'modified': fields.DateTime(readOnnly=True, description = 'date modified'),
    'user_id': fields.Integer(readOnly = True, description='User that made the category')
})

edit_category = api.model('Edit category',{
    'name': fields.String(required=False, description='Category name'),
    'description': fields.String(required = False, description = 'A brief description of the category')
})

category_collection = api.inherit('Categories collection', pagination, {
    'items': fields.List(fields.Nested(category))
})

category_with_recipes = api.inherit('Yummy category with recipes', category, {
    'recipes': fields.List(fields.Nested(recipes, required=True))
})


users = api.model('User', {
    'name': fields.String(required = True, description = 'Users name'),
    'username': fields.String(required = True,
       description = 'User unique name on the app'),
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
    'old_password': fields.String(required = True, description = 'User Password'),
    'new_password': fields.String(required = True, description = 'User Password')
})
