from flask import request
from flask_restplus import Resource

from app.api.yummy.utilities import register_user, user_login, user_logout
from app.api.yummy.serializers import users
from ...restplus import api
from app.models import User

ns = api.namespace('Users', description='Operations on Users')


@ns.route('/register')
class UserRegistration(Resource):


    @api.response(201, 'User sucessfully Registered')
    @api.expect(users)
    def post(self, data):
        """ Registers a user """
        data = request.json
        register_user(data)
        return None, 201



