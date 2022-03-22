from flask_app import create_app, db
from flask_migrate import Migrate
from flask_app.models import User


app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell():
    return dict(db=db, app=app, User=User)
