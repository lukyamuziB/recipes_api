import os
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager
from flask_sqlalchemy import SQLAlchemy

from config import config
from app import create_app, db
from app.models import User, Categories, Recipes


"""make flask app instance with development configurations"""

dev = config['development']
app = create_app(dev)

manager = Manager(app)
db = SQLAlchemy(app)
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
