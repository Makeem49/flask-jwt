from email import header
from lib2to3.pgen2 import token
from urllib import response
from flask import url_for
import json
from flask_app.models import User, BlackListToken
from time import sleep
from flask_app.extensions import db
from tests.conftest import client


class TestAuth():
    """
    Test authentiaction route
    """

    def test_registration(self, client):
        """Testing user registration route"""
        response = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='john@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully registered.'
        assert data['auth_token']
        assert response.content_type == 'application/json'
        assert response.status_code == 201

    def test_register_user_fail(self, client, db):
        """Fail to register a user if it is already in db"""
        user = User(
            email='joe@gmail.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()

        response = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='joe@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())

        assert data['status'] == 'fail'
        assert data['message'] == "User already exists. Please log in"
        assert response.content_type == 'application/json'
        assert response.status_code == 202

    def test_login_user(self, client):
        """Test for login user"""

        # reister user
        response_register = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='john123@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data_register = json.loads(response_register.data.decode())

        assert data_register['status'] == "success"
        assert data_register['message'] == "Successfully registered."
        assert data_register['auth_token']

        # login registered user
        response_login = client.post(url_for('auth.login'), data=json.dumps(dict(
            email='john123@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response_login.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully logged in.'
        assert data['auth_token']
        assert response_login.status_code == 200

    def test_login_fail_due_to_password(self, client):
        """Fail user if login is incorrect"""

        # register user
        response_register = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='mark009@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data_register = json.loads(response_register.data.decode())

        assert data_register['status'] == "success"
        assert data_register['message'] == "Successfully registered."
        assert data_register['auth_token']

        # login registered user
        response_login = client.post(url_for('auth.login'), data=json.dumps(dict(
            email='mark009@gmail.com',
            password='1234567'
        )),
            content_type="application/json"
        )

    def test_login_fail_due_to_email(self, client):
        """Return fail user if the email is not found in the db"""

        register_response = client.post(url_for('auth.login'), data=json.dumps(dict(
            email="user@gmail.com",
            password="hefelfhiuew"
        )))

        data = json.loads(register_response.data.decode())

        assert data['status'] == 'fail'
        assert data['message'] == 'Try again'

    def test_logout_user(self, client):
        """Testing the logout route function"""

        # reister user
        response_register = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='MarkAngel123@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data_register = json.loads(response_register.data.decode())

        assert data_register['status'] == "success"
        assert data_register['message'] == "Successfully registered."
        assert data_register['auth_token']

        # login registered user
        response_login = client.post(url_for('auth.login'), data=json.dumps(dict(
            email='MarkAngel123@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response_login.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully logged in.'
        assert data['auth_token']
        assert response_login.status_code == 200

        # logout test

        response_logout = client.post(url_for('auth.logout'), headers=dict(
            Authorization="Bearer " +
            json.loads(response_login.data.decode())["auth_token"]
        ))

        logout_data = json.loads(response_logout.data.decode())

        assert logout_data['status'] == 'success'
        assert logout_data['message'] == 'Successfully logged out.'
        assert response_logout.status_code == 200

    def test_logout_user_fail(self, client):
        """Testing the logout fail route function"""

        # reister user
        response = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='MarkAngel@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully registered.'
        assert data['auth_token']
        assert response.content_type == 'application/json'
        assert response.status_code == 201
        # login registered user
        response_login = client.post(url_for('auth.login'), data=json.dumps(dict(
            email='MarkAngel123@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response_login.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully logged in.'
        assert data['auth_token']
        assert response_login.status_code == 200

        # logout fail  test due to invalid token
        sleep(121)

        response_logout = client.post(url_for('auth.logout'), headers=dict(
            Authorization='Bearer ' +
            json.loads(response_login.data.decode())['auth_token']
        ))

        logout_data = json.loads(response_logout.data.decode())

        assert logout_data['status'] == 'fail'
        assert logout_data['message'] == "Signature expired. Please log in again"
        assert response_logout.status_code == 401

    def test_logout_blacklisted_token(self, client):
        """The test case ensure that a blacklisted token cannot log out because it has already log out before and a login message will be prompt"""

        # register user
        response = client.post(url_for('auth.register'), data=json.dumps(dict(
            email='MarkAngel1230@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully registered.'
        assert data['auth_token']
        assert response.content_type == 'application/json'
        assert response.status_code == 201
        # login registered user
        response_login = client.post(url_for('auth.login'), data=json.dumps(dict(
            email='MarkAngel1230@gmail.com',
            password='12345678'
        )),
            content_type="application/json"
        )

        data = json.loads(response_login.data.decode())

        assert data['status'] == 'success'
        assert data['message'] == 'Successfully logged in.'
        assert data['auth_token']
        assert response_login.status_code == 200

        # Blacklist a token before hitting the logout endpoint
        token_blacklist = BlackListToken(token=data['auth_token'])
        db.session.add(token_blacklist)
        db.session.commit()

        # When the interpreter get's here, the token is already blacklisted and will not be useful again, so a login message is return
        response_logout = client.post(url_for('auth.logout'), headers=dict(
            Authorization='Bearer ' +
            json.loads(response_login.data.decode())['auth_token']
        ))

        logout_data = json.loads(response_logout.data.decode())

        assert logout_data['status'] == 'fail'
        assert logout_data['message'] == 'Token blacklisted. Please log in again.'
        assert response_logout.status_code == 401
    
    def test_user_status_malformed_bearer_token(self, client):
        """This is to test user with malformed token i.e Athorization which the Bearer and the token has no space"""


        register_user = client.post(url_for("users.get_user"), data=json.dumps(
            email="markAngel@gmail.com",
            password = 'password'
        ))

        