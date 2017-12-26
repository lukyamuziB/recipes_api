from flask import request
from flask_restplus import Resource


from app.api.yummy.utilities import create_recipe, update_recipe, delete_recipe
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
        
        """ Returns paginated list of Recipes. """
    
        args = pagination_args.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        recipes_query = Recipes.query
        recipes_page = recipes_query.paginate(page, per_page, error_out=False)

        return recipes_page

    @api.expect(recipe)
    def post(self):
        
        """ Creates a Recipe """
        data = request.json
        usr_id = 18
        ctg_id = data.get('category_id')
        create_recipe(data, ctg_id, usr_id)
        return '{message: Sucessfuly created Recipe}', 201


@ns.route('/<int:id>')
@api.response(404, 'Recipe not found.')
class Recipe(Resource):

    @api.marshal_with(recipe)
    def get(self, id):
        
        """ Returns a specific Recipe identified by its id. """

        return Recipes.query.filter(Recipes.id == id).one()

    @api.expect(recipe)
    @api.response(204, 'Recipe successfully updated.')
    def put(self, id):
        
        """" Updates a Recipe. """
        
        data = request.json
        update_recipe(id, data)
        return None, 204

    @api.response(204, 'Recipe successfully deleted.')
    def delete(self, id):
        """
        Deletes a Recipe.
        """
        delete_recipe(id)
        return None, 204
