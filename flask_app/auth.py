from crypt import methods
from urllib import response
from flask import Blueprint, jsonify, make_response, request
from .models import User, BlackListToken
from flask_app.extensions import db
from sqlalchemy.exc import IntegrityError


auth = Blueprint('auth', __name__)


@auth.route('/registration', methods=['POST'])
def register():
    data = request.get_json()

    user = User.query.filter_by(email=data.get('email')).first()

    if not user:
        try:
            user = User(email=data.get('email'),
                        password=data.get('password'))

            # insert user
            db.session.add(user)
            db.session.commit()
            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            print(auth_token)
            print(auth_token.decode())

            response = {
                "status": 'success',
                "message": "Successfully registered.",
                "auth_token": auth_token.decode()
            }

            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {
                "status": "fail",
                'message': 'Some error occurred. Please try again.'
            }

            return make_response(jsonify(response)), 401

    else:
        response = {
            "status": "fail",
            "message": "User already exists. Please log in"
        }
        return make_response(jsonify(response)), 202


@auth.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    print(post_data)
    try:
        # fetch user
        user = User.query.filter_by(email=post_data.get('email')).first()

        if user:
            if user.verify_password(post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)

                if auth_token:
                    response = {
                        'status': "success",
                        'message': "Successfully logged in.",
                        "auth_token": auth_token.decode()
                    }

                    return make_response(jsonify(response)), 200

            else:
                return make_response(jsonify({
                    "message": "incorrect password"
                }))
        else:
            return make_response(*jsonify({
                'message': "User not found"
            }))
    except Exception as e:
        print(e)
        response = {
            "status": "fail",
            "message": "Try again"
        }

        return make_response(jsonify(response)), 500


@auth.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get("Authorization")

    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401

    else:
        auth_token = ''

    if auth_token:
        user = User.decode_user_token(auth_token)
        print(user)
        if not isinstance(user, str):
            black_listed_token = BlackListToken(auth_token)
            try:
                db.session.add(black_listed_token)
                db.session.commit()
                responseobject = {
                    'status': 'success',
                    'message': "Successfully logged out."
                }
                return make_response(jsonify(responseobject)), 200
            except IntegrityError as e:
                responseobject = {
                    "status": "fail",
                    'message': e
                }
                return make_response(jsonify(responseobject)), 200
        else:
            responseobject = {
                'status': 'fail',
                'message': user
            }

            return make_response(jsonify(responseobject)), 401
    else:
        responseobject = {
            'status': "fail",
            "message": 'Provide a valid auth token.'
        }

        return make_response(jsonify(responseobject)), 403
