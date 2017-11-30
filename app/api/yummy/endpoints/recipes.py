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

        posts_query = Recipes.query
        recipes_page = posts_query.paginate(page, per_page, error_out=False)

        return recipes_page

    @api.expect(recipe)
    def post(self):
        
        """ Creates a Recipe """
        
        create_recipe(request.json)
        return None, 201


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

''' 
@ns.route('/archive/<int:year>/')
@ns.route('/archive/<int:year>/<int:month>/')
@ns.route('/archive/<int:year>/<int:month>/<int:day>/')
class PostsArchiveCollection(Resource):

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(page_of_blog_posts)
    def get(self, year, month=None, day=None):
        """
        Returns list of blog posts from a specified time period.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        start_month = month if month else 1
        end_month = month if month else 12
        start_day = day if day else 1
        end_day = day + 1 if day else 31
        start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
        end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)
        posts_query = Recipes.query.filter(Recipes.pub_date >= start_date).filter(Recipes.pub_date <= end_date)

        posts_page = posts_query.paginate(page, per_page, error_out=False)

        return posts_page
    
    '''
