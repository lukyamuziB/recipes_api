from flask_script import Shell, Manager
from config import config
from app import create_app, db
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Categories, Recipes
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

"""make flask app instance with development configurations"""

dev = config['development']
app = create_app(dev)

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# def shell_context():
#     return dict(app=app, db = db, User = User, Categories = Categories, Recipes = Recipes)


# manager.add_command("shell", Shell(make_context=shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
    db.create_all()