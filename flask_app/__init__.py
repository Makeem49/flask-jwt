from flask import Flask
import os
from flask_app.views import users
from .auth import auth
from flask_app.extensions import db, migrate

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(settings_override=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')

    if settings_override is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        """
            app.config.update() help to update settings.py file in the config file 
        """
        app.config.update(settings_override)
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///' +
                          os.path.join(basedir, 'flask_jwt_test.sqlite'))
        app.config.update(SERVER_NAME="localhost.localdomain:5000")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(users)
    app.register_blueprint(auth)

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance 
    :return : None
    """
    db.init_app(app)
    migrate.init_app(app)

    return None
