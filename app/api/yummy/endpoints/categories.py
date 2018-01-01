from flask import request
from flask_restplus import Resource


from app.api.yummy.utilities import create_category,\
      delete_category, update_category
from app.api.yummy.serializers import category,\
 category_with_recipes, category_collection
from app.api.yummy.parsers import pagination_args 
from ...restplus import api
from app.models import Categories


ns = api.namespace('Categories', \
  description='Operations related to Recipe Categories')


@ns.route('/')
class CategoryCollection(Resource):

    
    @api.expect(pagination_args)
    @api.marshal_list_with(category_collection)
    def get(self):
    
        """ Returns a paginated list of categories"""
        
        args = pagination_args.parse_args(request)
        query = args.get('q')
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        if query is None:
            category_query = Categories.query
        else:
            category_query = Categories.query.filter_by(name = query) 

        categories_page = category_query.paginate(page, per_page,
                    error_out = False)
        
        return categories_page

    @api.response(201, 'Category successfully created.')
    @api.response(409, 'Conflict, Category already exists')
    @api.expect(category)
    def post(self):
       
        """ Creates a new  category. """
        user_id = 4
        data = request.json
        try:
            create_category(data, user_id)
            return '{message: Sucessfuly created category}', 201
        except ValueError as e:
            return "{Error: You are creating an already existent Category}",409



@ns.route('/<int:id>')
@api.response(404, 'The Category you are querying does not exist.')
class CategoryItem(Resource):

    @api.marshal_with(category_with_recipes)
    def get(self, id):
    
        """ Returns a category with all Recipes associated with it """
        
        return Categories.query.filter(Categories.id == id).first()

    @api.expect(category)
    @api.response(204, 'Category successfully updated.')
    def put(self, id):
        """
        * Updates a category in the Yummy recipes database
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        try:
            update_category(id, data)
            return '{message: Category successfully updated}', 204
        except ValueError as e:
            return "{Error: Can't edit non existent Category}",404


    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        
        """ Deletes a Recipe Category. """

        try:
            delete_category(id)
            return "{Successful: Deleted Category}", 204
        except ValueError as identifier:
            return "{Error: Can't delete non exixtent Category}",404
        

