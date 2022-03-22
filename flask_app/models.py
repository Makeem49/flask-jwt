from datetime import datetime, timedelta
from enum import unique
from werkzeug.security import check_password_hash, generate_password_hash
from flask_app.extensions import db
import jwt
from flask import current_app


class User(db.Model):
    """User Model for storing user related details"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    registered_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password():
        raise AttributeError('Password field is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """Generate token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=120),
                "iat": datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_user_token(auth_token):
        """
        Deocde the auth token
        :param auth_token: bytes
        :return: integer|string
        """

        try:
            payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
            if BlackListToken.check_blacklisted_token(auth_token):
                return 'Token blacklisted. Please log in again.'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again"
        except jwt.InvalidTokenError:
            return "Invalid token. Please login again."


class BlackListToken(db.Model):
    """This schema represent blacklisted token the are valid"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token) -> None:
        super().__init__()
        self.token = token
        self.blacklisted_on = datetime.now()

    @staticmethod
    def check_blacklisted_token(token):
        black_list_token = BlackListToken.query.filter_by(token=token).first()
        if black_list_token:
            return True
        return False

    def __repr__(self) -> str:
        return f"token {self.token}"


