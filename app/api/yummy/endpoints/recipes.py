from flask import request
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound


from app.api.yummy.utilities import create_recipe,\
       update_recipe, delete_recipe
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

        recipes_page = recipes_query.paginate(page,
              per_page, error_out = False)  

        return recipes_page

    
    @api.response(404, 'Category Not found')
    @api.response(409, 'Conflict, Recipe already exists')
    @api.response(201, 'Successful, Recipe Created')
    @api.expect(recipe)
    def post(self):
        
        """ Creates a Recipe """
        data = request.json
        usr_id = 18
        ctg_id = data.get('category_id')
        try:
            create_recipe(data, ctg_id, usr_id)
            return '{message: Sucessfuly created Recipe}', 201
        except ValueError as e:
            return "{Error: You are creating an already existent Recipe}",409
        except NoResultFound as e:
            return "{Error: Recipe can't belong to non existent Category}",404




@ns.route('/<int:id>')
@api.response(404, 'Recipe not found.')
class Recipe(Resource):

    @api.marshal_with(recipe)
    def get(self, id):
        
        """ Returns a specific Recipe identified by its id. """

        return Recipes.query.filter_by(id = id).first()

    
    @api.expect(recipe)
    @api.response(204, 'Recipe successfully updated.')
    def put(self, id):
        
        """ Updates a Recipe. """
    
        data = request.json
        try:
            update_recipe(id, data)
            return "{Successful: Recipe successfully updated}", 204
        except ValueError as e:
            return "{Error: can't edit a non existent recipe}",404


    @api.response(204, 'Recipe successfully deleted.')
    def delete(self, id):
        """
        Deletes a Recipe.
        """
        try:
            delete_recipe(id)
            return '{message: Recipe successfully deleted}', 204
        except ValueError as e:
            return "{Error: Can't delete non existent Recipe}",404
            

