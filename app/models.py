from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    recipes = db.relationship('Recipes', backref = 'user', lazy = 'dynamic')
    categories = db.relationship('Categories', backref = 'user', lazy = 'dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column( db.Integer, primary_key = True, autoincrement = True)
    name = db.Column( db.String(50), unique = True)
    description = db.Column( db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    recipes = db.relationship('Recipes', backref = 'category', lazy = 'dynamic')


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), unique = True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False )
