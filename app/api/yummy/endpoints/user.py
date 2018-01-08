from flask import request
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.api.yummy.utilities import (
    register_user, user_login, user_logout,
    reset_password, change_username
    
)
from app.api.yummy.serializers import (
    users, usr,
    users_password_reset, username_reset
)

from ...restplus import api
from app.models import User

ns = api.namespace('auth', description='Operations on User Authentication')


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
            return "{\nSuccess: user Successfuly loged in\nToken: a\n}",200
        except NoResultFound as e:
            return "{Error: Username is not Registered}",404
        except ValueError as e:
            return "{Error: Wrong Password}",404

@ns.route('/reset_password')
class UserPasswordReset(Resource):

    @api.response(200, 'Password Successfully Reset')
    @api.expect(users_password_reset)
    @jwt_required
    def put(self):
        """ Resets a User's password """
        
        data = request.json
        id = get_jwt_identity()
        reset_password(data, id)
        return "{Successful: Password successfully reset}",200


@ns.route('/change_username')
class UsernameReset(Resource):

    @api.expect(username_reset)
    @api.response(200, 'Username Successfully changed')
    @jwt_required
    def put(self):
        """Resets a user's username """

        data = request.json
        id = get_jwt_identity
        change_username(data, id)
        return "{Successful: Username Successfully changed}",200

@ns.route('/logout')
class UserLogout(Resource):
    @api.response(200, "Successfully loged out")
    @jwt_required
    def delete(self):
        """ logs out a user """
        user_logout()
        return "{Message: Successfully loged out}",200


        





