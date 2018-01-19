#third import imports
from flask import request, jsonify, make_response
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, jwt_optional
)


#local imports
from app.exceptions import (
    ResourceAlreadyExists, YouDontOwnResource,
    EmailEmpty, PasswordEmpty, UsernameEmpty, NameEmpty,
    WrongPassword, UsernameEmpty,PasswordFormatError,
     EmailFormatError, UsernameFormatError
   )
from app.api.utilities import (
    register_user, user_login, user_logout,
    reset_password, change_username 
)
from app.api.serializers import (
    users, usr,
    users_password_reset, username_reset
)
from app.api.restplus import api
from app.models import User


ns = api.namespace('auth', description='Operations on User Authentication')


@ns.route('/register')
class UserRegistration(Resource):

    @api.response(201, 'User sucessfully Registered')
    @api.response(409, 'Conflict, User already exists')
    @api.response(400, 'Bad request, cant post data with empty fields')
    @api.expect(users)
    def post(self):
        """ Registers a user """
        data = request.json
        try:
            register_user(data)
            return make_response(jsonify(
                   {"Message": "User Sucessfully Registered"}), 201)
        except ResourceAlreadyExists:
            return make_response(jsonify(
                   {"Error": "User already exists"}),409)
        except NameEmpty:
            return make_response(jsonify(
                  {"Error": "Name Can't be Empty"}), 400)
        except UsernameEmpty:
            return make_response(jsonify(
                  {"Error": "Username Can't be Empty"}), 400)
        except EmailEmpty:
            return make_response(jsonify(
                  {"Error": "Email Can't be Empty"}), 400)
        except PasswordEmpty:
            return make_response(jsonify(
                  {"Error": "Password Can't be Empty"}), 400)
        except PasswordFormatError:
            return make_response(jsonify(
                  {"Error": "Make sure your password is at least 6 alphanumeric characters"}), 400)
        except UsernameFormatError:
            return make_response(jsonify(
                  {"Error": "Make sure your username is only alphanumeric"}), 400)
        except EmailFormatError:
            return make_response(jsonify(
                  {"Error": "Enter your Email in the correct format"}), 400)
        
               
@ns.route('/login')
class UserLogin(Resource):
    
    @api.response(200, 'User sucessfully Loged in')
    @api.response(404, 'User not registered')
    @api.response(400, 'Bad Request')
    @api.expect(usr)
    def post(self):
        """ logs in a registered user """
        data = request.json
        try:
            token = user_login(data) 
            return make_response(jsonify(
               {'Message': 'Successfuly loged in',
        'token':token}),200)
        except NoResultFound:
            return make_response(jsonify(
              {'Error':'Username is not Registered'}),404)
        except WrongPassword:
            return make_response(jsonify(
              {'Error': 'Wrong Password'}),404)
        except PasswordEmpty:
            return make_response(jsonify(
              {'Error': 'Provide your password to login'}),400)
        except UsernameEmpty:
            return make_response(jsonify(
              {'Error': 'Provide your username to login'}),400)


@ns.route('/change_password')
class UserPasswordReset(Resource):

    @api.response(200, 'Password Successfully Reset')
    @api.expect(users_password_reset)
    @jwt_required
    def put(self):
        """ Resets a User's password """
        
        data = request.json
        id = get_jwt_identity()
        try:
            reset_password(data, id)
            return make_response(jsonify(
                {'Message': 'Password successfully reset'}),200)
        except ValueError:
            return make_response(jsonify(
            {'Error':"Enter your old password correctly to reset Password"}))


@ns.route('/change_username')
class UsernameReset(Resource):

    @api.expect(username_reset)
    @api.response(200, 'Username Successfully changed')
    @jwt_required
    def put(self):
        """Resets a user's username """

        data = request.json
        id = get_jwt_identity()
        change_username(data, id)
        return make_response(jsonify(
               {"Message": "Username Successfully changed"}),200)


@ns.route('/logout')
class UserLogout(Resource):
    @api.response(200, "Successfully loged out")
    @jwt_required
    def delete(self):
        """ logs out a user """
        user_logout()
        return make_response(jsonify(
               {"Message": "Successfully loged out"}),200)
