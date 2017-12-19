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


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
