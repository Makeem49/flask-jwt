from flask_app.models import User
from flask_app.models import BlackListToken


class TestUserModel():
    """Test for user model"""

    def test_add_user_to_db(self, db):
        user = User(
            email='test1@test.com',
            password='test'
        )

        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token(user.id)
        assert isinstance(auth_token, bytes)
        assert User.decode_user_token(auth_token) == 9

    def test_token_decode_and_encode(self, db):
        """Testing the token in bytes and integer for the payload"""

        user = User(
            email='test12@test.com',
            password='test'
        )

        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token(user.id)

        assert isinstance(auth_token, bytes)
        assert (User.decode_user_token(auth_token.decode('utf-8')) == 10)
