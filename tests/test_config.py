from flask import current_app
from flask_app.models import User

class TestConfig():
    """Testing app configuration"""

    def test_debug(self, app):
        """Testing debug variable"""

        assert app.config['DEBUG'] is False

    def test_db_connection(self, app, db):
        """Testing db connection"""

        assert app.config['SQLALCHEMY_DATABASE_URI'] != "/flask-jwt/flask_app/flask_jwt_test.sqlite"

    def test_current_app(self):
        """Test current app"""
        assert current_app is not None

    def test_secret_key(self):
        """Testing secret key"""
        assert current_app.config['SECRET_KEY'] == 'HNDIVUCHFSKHIU'


