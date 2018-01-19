from flask import request, jsonify, make_response
from flask_restplus import Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm.exc import NoResultFound

from app.exceptions import ResourceAlreadyExists, EmptyField, EmptyDescription
from app.api.utilities import (create_category,
      delete_category, update_category)
from app.api.serializers import (category,
     category_with_recipes, category_collection,
     edit_category
)
from app.api.parsers import pagination_args 
from app.api.restplus import api
from app.models import Categories


ns = api.namespace('categories', \
  description='Operations related to Recipe Categories')


@ns.route('')
class CategoryCollection(Resource):

    @jwt_required
    @api.expect(pagination_args)
    def get(self):
    
        """ Returns a paginated list of categories"""
        
        args = pagination_args.parse_args(request)
        query = args.get('q')
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        user_id = get_jwt_identity()


        if query is None:
            category_query = Categories.query.filter_by(user_id = user_id)
        else:
            category_query = Categories.query.filter(
                Categories.name.ilike("%"+query+"%"), Categories.user_id == user_id)

        categories_page = category_query.paginate(page, per_page,
                    error_out = False)
        
        if not categories_page.items:
            return make_response(jsonify(
        {"Error":f"This page doesn't have any categories yet"}))
        else:
            return marshal(categories_page, category_collection)

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
            return make_response(jsonify(
                    {"Message": "Sucessfuly created category"}), 201)
        except ResourceAlreadyExists:
            return make_response(jsonify(
                   {"Error": "You are creating an already existent Category"}),409)


@ns.route('/<int:id>')
@api.response(404, 'The Category you are querying does not exist.')
class CategoryItem(Resource):
    
    @jwt_required
    def get(self, id):
    
        """ Returns a category with all Recipes associated with it """
        user_id = get_jwt_identity()
        response = Categories.query.filter_by( 
            id = id, user_id = user_id).first()
        if response is None:
            print("reaching here")
            return make_response(jsonify(
                   {"Error": "We didnt find any category coresponding to the id you provided"}), 400)
        return marshal(response, category_with_recipes)


    @api.expect(edit_category)
    @jwt_required
    @api.response(204, 'Category successfully updated.')
    @api.response(404, "Not Found, Category doesn't exist")
    @api.response(400, "Bad Request.")
    def put(self, id):
        """
        * Updates a category in the Yummy recipes database
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        a = get_jwt_identity()
        try:
            update_category(id, data)
            return make_response(jsonify(
                   {"Message": "Category successfully updated"}), 200)
        except NoResultFound as e:
            return make_response(jsonify(
                   {"Error": "Can't edit non existent Category"}),404)
        except EmptyField:
            return make_response(jsonify(
                   {"Error": "Category name field cant be left empty"}),400)
        except EmptyDescription:
            return make_response(jsonify(
            {"Error": "Category description field cant be left empty"}),400)


    @api.response(200, 'Category successfully deleted.')
    @api.response(404, 'Not Found, Category does not exixt')
    @api.response(403, "Forbidden, You don't own this category")
    @jwt_required
    def delete(self, id):
        
        """ Deletes a Recipe Category. """
        user_id = get_jwt_identity()
        try:
            delete_category(id, user_id)
            return make_response(jsonify(
                    {"Message": "Successfully Deleted Category"}),200)
        except NoResultFound as identifier:
            return make_response(jsonify(
                    {'Error': "Can't delete non existent Category"}),404)
        except YouDontOwnResource as e:
            return make_response(jsonify(
                   {'Error': "Can't delete a recipe a you did not create"}),403)

