from flask import request, jsonify
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.api.yummy.utilities import (create_recipe, 
                                update_recipe, delete_recipe)
from app.api.yummy.serializers import recipe, recipe_collection
from app.api.yummy.parsers import pagination_args
from app.api.restplus import api
from app.models import Recipes



ns = api.namespace('Recipes', description='Operations on Recipes')


@ns.route('/')
class RecipesCollection(Resource):

    @api.expect(pagination_args)
    @api.marshal_with(recipe_collection)
    def get(self):
        
        """ Returns a paginated list of Recipes. """
    
        args = pagination_args.parse_args(request)
        query = args.get('q')
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        
        if query is None:
            recipes_query = Recipes.query
        else:
            recipes_query = Recipes.query.filter_by(name = query)
            # (func.lower(Recipes.name == query)

        recipes_page = recipes_query.paginate(page,
              per_page, error_out = False)  

        return recipes_page

    
    
    @api.response(404, 'Category Not found')
    @api.response(409, 'Conflict, Recipe already exists')
    @api.response(201, 'Successful, Recipe Created')
    @jwt_required
    @api.expect(recipe)
    def post(self):
        
        """ Creates a Recipe """
        data = request.json
        usr_id = get_jwt_identity()
        ctg_id = data.get('category_id')
        try:
            create_recipe(data, ctg_id, usr_id)
            return jsonify({"Message": "Sucessfuly created Recipe"}), 201
        except ValueError as e:
            return jsonify({"Error": "You are creating an already existent Recipe"}),409
        except NoResultFound as e:
            return jsonify({"Error": "Recipe can't belong to non existent Category"}),404

{'message': 'You must be logged in to access this page'}
@ns.route('/<int:id>')
@api.response(404, 'Recipe not found.')
class Recipe(Resource):

    @api.marshal_with(recipe)
    def get(self, id):
        
        """ Returns a specific Recipe identified by its id. """

        return Recipes.query.filter_by(id = id).first()

    
    @api.expect(recipe)
    @jwt_required
    @api.response(204, 'Recipe successfully updated.')
    @api.response(404, 'Recipe does not exit')
    @api.response(403, 'Forbidden, You dont own this Recipe')
    def put(self, id):
        
        """ Updates a Recipe. """
    
        data = request.json
        try:
            update_recipe(id, data)
            return jsonify({"Message": "Recipe successfully updated"}), 204
        except ValueError as e:
            return sonify({"Error": "Can't edit non existent recipe"}),404
        except TypeError as e:
            return jsonify({"Error": "Can't edit a recipe you didnt create"}),403


    @jwt_required
    @api.response(200, 'Recipe successfully deleted.')
    @api.response(404, 'Recipe non existent')
    @api.response(403, 'Forbidden, You dont own this Recipe')
    def delete(self, id):
        """
        Deletes a Recipe.
        """

        try:
            delete_recipe(id)
            return jsonify({"Message": "Recipe successfully deleted"}), 200
        except ValueError as e:
            return jsonify({"Error": "Can't delete non existent Recipe"}),404
        except TypeError as e:
            return jsonify({"Error": "Can't delete a recipe you didnt create"}),403
            