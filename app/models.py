from . import db

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column( db.Integer, primary_key = True, autoincrement = True)
    name = db.Column( db.String(50), unique = True)
    description = db.Column( db.String(200))


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), unique = True)
    description = db.Column(db.String(200))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)


