from flask import make_response, jsonify
from .import api_v1

""" 
   this file handles custom error messages 
   and responses that are genaeral to the entire API
"""
@api_v1.app_errorhandler(404)
def not_found(e):
    return make_response(jsonify({'Error':"This is not the page you\
 were looking for, Enter a correct endpoint"}),404)


@api_v1.app_errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify({'Error':"We experienced an internal\
       Server Error, Try again later "}),500)