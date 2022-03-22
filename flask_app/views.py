from crypt import methods
import json
from traceback import print_tb
from urllib import response
from flask import Blueprint, jsonify, request, make_response
from pyparsing import restOfLine
from flask_app.models import User

users = Blueprint('users', __name__)


@users.route("/user", methods=['GET'])
def get_user():
    auth_header = request.headers.get('Authorization')
    print(auth_header)

    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            reponseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_user_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()

            responseObject = {
                "status": "success",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "admin": user.admin,
                    'registered_on': user.registered_on
                }
            }

            return make_response(jsonify(responseObject)), 200

        responseObject = {
            'status': 'fail',
            'message': resp
        }

        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            "status": "fail",
            "message": "Provide a valid auth token."
        }

        return make_response(jsonify(responseObject)), 401
