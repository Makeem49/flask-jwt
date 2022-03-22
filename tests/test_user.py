from email import header
from flask import url_for
import json
from flask_app.models import User


class TestUser():
    """Testing user route"""

    def test_user_status(self, client):
        """Get a particular user through the token pass to the header"""

        # Register a user
        register = client.post(url_for('auth.register'), data=json.dumps(dict(
            email="cynthia@gmail.com",
            password="123456789"
        )),
            content_type="application/json"
        )

        data = json.loads(register.data.decode())

        assert data['status'] == "success"
        assert data['message'] == "Successfully registered."
        assert data['auth_token']
        # print(data['auth_token'], "token value")

        get_response = client.get(url_for('users.get_user'), headers=dict(
            Authorization="Bearer " +
            json.loads(register.data.decode())["auth_token"]
        ))

        print(get_response.data.decode())
        data = json.loads(get_response.data.decode())

        assert data['status'] == 'success'
        assert data['data'] is not None
        assert data['data']['email'] == 'cynthia@gmail.com'
        assert data['data']['admin'] is False or True
        assert get_response.status_code == 200


    

