from flask import request, jsonify
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.api.yummy.utilities import create_category,\
      delete_category, update_category
from app.api.yummy.serializers import category,\
 category_with_recipes, category_collection
from app.api.yummy.parsers import pagination_args 
from ...restplus import api
from app.models import Categories


ns = api.namespace('categories', \
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
    @jwt_required
    def post(self):
       
        """ Creates a new  category. """

        user_id = get_jwt_identity()
        data = request.json
        try:
            create_category(data, user_id)
            return jsonify({"Message": "Sucessfuly created category"}), 201
        except ValueError as e:
            return jsonify({"Error": "You are creating an already existent Category"}),409



@ns.route('/<int:id>')
@api.response(404, 'The Category you are querying does not exist.')
class CategoryItem(Resource):

    @api.marshal_with(category_with_recipes)
    def get(self, id):
    
        """ Returns a category with all Recipes associated with it """
        
        return Categories.query.filter(Categories.id == id).first()

    @api.expect(category)
    @jwt_required
    @api.response(204, 'Category successfully updated.')
    @api.response(404, "Not Found, Category doesn't exist")
    @api.response(403, "Forbidden, You don't own this category")
    def put(self, id):
        """
        * Updates a category in the Yummy recipes database
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        a = get_jwt_identity()
        print(a)
        print("dfhgjdg")
        try:
            update_category(id, data)
            return jsonify({"Message": "Category successfully updated"}), 200
        except ValueError as e:
            return jsonify({"Error": "Can't edit non existent Category"}),404
        except TypeError as e:
            return jsonify({"Error": "Can't Edit a Category a you didn't create"}),403


    @api.response(204, 'Category successfully deleted.')
    @api.response(404, 'Not Found, Category does not exixt')
    @api.response(403, "Forbidden, You don't own this category")
    @jwt_required
    def delete(self, id):
        
        """ Deletes a Recipe Category. """

        try:
            delete_category(id)
            return jsomnify({"Message": "Deleted Category"}), 200
        except ValueError as identifier:
            return jsonify({"Error": "Can't delete non exixtent Category"}),404
        except TypeError as e:
            return jsonify({"Error": "Can't delete a recipe a you didn't create"}),403

