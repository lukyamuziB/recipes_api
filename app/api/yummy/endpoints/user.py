from flask import request
from flask_restplus import Resource

from app.api.yummy.utilities import register_user, user_login, user_logout
from app.api.yummy.serializers import users, usr
from ...restplus import api
from app.models import User

ns = api.namespace('Users', description='Operations on User Authentication')


@ns.route('/register')
class UserRegistration(Resource):


    @api.response(201, 'User sucessfully Registered')
    @api.expect(users)
    def post(self):
        """ Registers a user """
        data = request.json
        register_user(data)
        return '{message: User Sucessfully Registered}', 201

@ns.route('/login')
class UserLogin(Resource):
    
    @api.response(200, 'User sucessfully Loged in')
    @api.expect(usr)
    def get(self):
        """ logs in a registered user """
        data = request.json
        logi_user(data)
        return '{ message: Successfully Loged in user }', 200





