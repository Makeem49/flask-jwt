from flask_app import create_app
import pytest
from flask_app.models import User
from flask_app import db as _db



@pytest.fixture(scope='session')
def app():
    '''
        Setting up flask test app, this only get executed at the 
        beginning of the session 

        :param: None
        :return : flask app 
        '''
    params = {
        'TESTING': True,
        'DEBUG': False,
    }

    _app = create_app(params)

    ctx = _app.app_context()

    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    '''
    Set up a text client which execute per client
    :param: pytest fixture
    :return: None 
    '''
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def db(app):
    """
        Setup database, this only get executed once in a session
        :param: pytest fixture 
        :return : SQLAlchemy database session
        """
    # create a db table
    _db.drop_all()
    _db.create_all()

    admin = {
        "email": 'admin@gmail.com',
        "password": "password"
    }

    admin = User(**admin)

    _db.session.add(admin)
    _db.session.commit()

    return _db

