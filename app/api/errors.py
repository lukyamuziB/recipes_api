from flask import make_response, jsonify
from .import api_v1

""" 
   this file handles custom error messages 
   and responses that are genaeral to the entire API
"""
@api_v1.app_errorhandler(404)
def not_found(e):
    return make_response(jsonify({'Error':'This is not\
 the page youare looking for Enter a correct endpoint'}),404)


@api_v1.app_errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify({'Error':"We experienced an internal\
       Server Error, Try again later "}),500)


@api_v1.app_errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify(
    {'Error':"Request URL does not suppor this method "}),405)


@api_v1.app_errorhandler(400)
def bad_request(e):
    return make_response(jsonify({"Error":"we trying this"}),400)
