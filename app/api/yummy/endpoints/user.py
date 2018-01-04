from flask import request
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound

from app.api.yummy.utilities import register_user, user_login, user_logout
from app.api.yummy.serializers import users, usr
from ...restplus import api
from app.models import User

ns = api.namespace('Users', description='Operations on User Authentication')


@ns.route('/register')
class UserRegistration(Resource):


    @api.response(201, 'User sucessfully Registered')
    @api.response(409, 'Conflict, User already exists')
    @api.expect(users)
    def post(self):
        """ Registers a user """
        data = request.json
        try:
            register_user(data)
            return '{message: User Sucessfully Registered}', 201
        except ValueError as e:
            return "{Error: User already exists}",409


@ns.route('/login')
class UserLogin(Resource):
    
    @api.response(200, 'User sucessfully Loged in')
    @api.response(404, 'User not registered')
    @api.expect(usr)
    def post(self):
        """ logs in a registered user """
        data = request.json
        try:
            a = user_login(data) 
            print(a)
            return "{\nSuccess: user Successfuly loged in\nToken: + a\n}",200
        except NoResultFound as e:
            return "{Error: Username is not Registered}",404
        except ValueError as e:
            return "{Error: Wrong Password}",404
        





