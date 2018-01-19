#third party imports
from flask import request, jsonify, make_response
from flask_restplus import Resource, marshal
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.exceptions import ResourceAlreadyExists, YouDontOwnResource

#local imports
from app.api.utilities import (create_recipe, 
                                update_recipe, delete_recipe)
from app.api.serializers import (recipes,
    recipe_collection, edit_recipe)
from app.api.parsers import pagination_args
from app.api.restplus import api
from app.models import Recipes


ns = api.namespace('recipes', description='Operations on Recipes')


@ns.route('')
class RecipesCollection(Resource):
    
    @jwt_required
    @api.expect(pagination_args)
    def get(self):
        
        """ Returns a paginated list of Recipes. """
        
        user_id = get_jwt_identity()
        args = pagination_args.parse_args(request)
        query = args.get('q')
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        user_id =get_jwt_identity()
        if query is None:
            recipes_query = Recipes.query.filter_by(user_id = user_id)
        else:
            recipes_query = Recipes.query.filter(
                            Recipes.name.ilike(
                                "%"+query+"%"), Recipes.user_id == user_id)
        recipes_page = recipes_query.paginate(page,
              per_page, error_out = False) 

        if not recipes_page.items:
            return make_response(jsonify(
        {"Error":f"Page {page} doesn't have any recipes yet"}),400)
        else:
            return marshal(recipes_page, recipe_collection)


    @api.response(404, 'Category Not found')
    @api.response(409, 'Conflict, Recipe already exists')
    @api.response(201, 'Successful, Recipe Created')
    @jwt_required
    @api.expect(recipes)
    def post(self):
        
        """ Creates a Recipe """
        data = request.json
        usr_id = get_jwt_identity()
        ctg_id = data.get('category_id')
        try:
            create_recipe(data, ctg_id, usr_id)
            return make_response(jsonify(
                   {"Message": "Sucessfuly created Recipe"}), 201)
        except ResourceAlreadyExists as e:
            return make_response(jsonify(
            {"Error": "You are creating an already existent Recipe"}),409)
        except NoResultFound as e:
            return make_response(jsonify(
            {"Error": "Recipe can't belong to non existent Category"}),404)


@ns.route('/<int:id>')
@api.response(404, 'Recipe not found.')
class Recipe(Resource):
    
    @jwt_required
    def get(self, id):
        """ Returns a specific Recipe identified by its id. """
        user_id = get_jwt_identity()
        response = Recipes.query.filter_by(
             id = id, user_id = user_id).first()
        if response is None:
            return make_response(jsonify(
                   {"Error": "We didnt find any Recipe\
                    coresponding to the id you provided"}), 400)
        return marshal(response, recipes)
    
    @api.expect(edit_recipe)
    @jwt_required
    @api.response(204, 'Recipe successfully updated.')
    @api.response(404, 'Recipe does not exit')
    @api.response(403, 'Forbidden, You dont own this Recipe')
    def put(self, id):
        """ Updates a Recipe. """
    
        data = request.json
        try:
            update_recipe(id, data)
            return make_response(jsonify(
                   {"Message": "Recipe successfully updated"}), 204)
        except NoResultFound:
            return make_response(jsonify(
                   {"Error": "Can't edit non existent recipe"}),404)
        except YouDontOwnResource:
            return make_response(jsonify(
                   {"Error": "Can't edit a recipe you didnt create"}),403)


    @jwt_required
    @api.response(200, 'Recipe successfully deleted.')
    @api.response(404, 'Recipe non existent')
    @api.response(403, 'Forbidden, You dont own this Recipe')
    def delete(self, id):
        """
        Deletes a Recipe.
        """
        user_id = get_jwt_identity()
        try:
            delete_recipe(id, user_id)
            return make_response(jsonify(
                   {"Message": "Recipe successfully deleted"}), 200)
        except NoResultFound:
            return make_response(jsonify(
                   {"Error": "Can't delete non existent Recipe"}),404)
        except YouDontOwnResource:
            return make_response(jsonify(
                   {"Error": "Can't delete a recipe you didnt create"}),403)
            