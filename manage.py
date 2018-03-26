import os
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import config
from app import create_app, db
from app.models import User, Categories, Recipes


"""make flask app instance with development configurations"""

# dev = os.getenv('FLASK_CONFIG')
app = create_app(config_name=os.getenv('FLASK_CONFIG'))

manager = Manager(app)
db = SQLAlchemy(app)
CORS(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Recipes = Recipes,
               Categories = Categories)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    os.system("pytest --cov-report term --cov=app")


@manager.command
def debug_tests():
    os.system("pytest --ipdb")


if __name__ == '__main__':
    manager.run()
