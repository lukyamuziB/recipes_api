import logging

from flask import request
from flask_restplus import Resource
from app.api.yummy.utilities import create_category, delete_category, update_category
from app.api.yummy.serializers import category, category_with_posts
from ...restplus import api
from app.models import Categories

log = logging.getLogger(__name__)

ns = api.namespace('/categories', description='Operations related to yummy categories')


@ns.route('/')
class CategoryCollection(Resource):

    @api.marshal_list_with(category)
    def get(self):
    
        """ Returns list of categories"""

        categories = Categories.query.all()
        return categories

    @api.response(201, 'Category successfully created.')
    @api.expect(category)
    def post(self):
       
        """ Creates a new  category. """
     
        data = request.json
        create_category(data)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'The Category you are querying does not exist.')
class CategoryItem(Resource):

    @api.marshal_with(category_with_posts)
    def get(self, id):
    
        """ Returns a category with a list of all Recipes under it. """
        
        return Categories.query.filter(Category.id == id).one()

    @api.expect(category)
    @api.response(204, 'Category successfully updated.')
    def put(self, id):
        """
        * Updates a category in the Yummy recipes database
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        update_category(id, data)
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        
        """ Deletes blog category. """
        
        delete_category(id)
        return None, 204
