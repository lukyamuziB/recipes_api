from flask_restplus import fields
from app.api.restplus import api

recipe = api.model('Blog post', {
    'id': fields.Integer(readOnly=True, description='recipe unique identifier'),
    'name': fields.String(required=True, description='recipe name'),
    'description': fields.String(required=True, description='A brief description of the recipes'),
    'recipe steps': fields.String(required = True, descripton = 'Procedure/ Steps of the Recipe'
    'category_id': fields.Integer(attribute='category.id'),
    'category': fields.String(attribute='category.id'),
})

recipe_collection = api.inherit('Page of blog posts', pagination, {
    'items': fields.List(fields.Nested(recipe))
})

category = api.model('Blog category', {
    'id': fields.Integer(readOnly=True, description='Unqiue category Id for Identity purposes'),
    'name': fields.String(required=True, description='Category name'),
    'description': fileds.String(required = True, description = 'A brief description of the category')
})

category_with_recipes = api.inherit('Yummy category with recipes', category, {
    'category': fields.List(fields.Nested(blog_post))
})
