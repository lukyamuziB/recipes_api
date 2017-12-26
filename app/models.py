from werkzeug.security import generate_password_hash, check_password_hash
from random import seed, randint
import forgery_py
from sqlalchemy.exc import IntegrityError
from . import db


class User(db.Model):
    """user database modeal"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    recipes = db.relationship('Recipes', backref = 'user', lazy = 'dynamic')
    categories = db.relationship('Categories', backref = 'user', lazy = 'dynamic')

    """makes the password colum impossible to querry """
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    """ Function to generate fake users for testing the API at a large scale"""
    @staticmethod
    def data_generator(count=200):
        seed()
        num = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, num)).first()
            c = Categories(name=forgery_py.lorem_ipsum.word(),
            description=forgery_py.lorem_ipsum.sentence(),
            user= u)
            db.session.add(c)
            try:
                db.session.commit()
                print("sucessful")
            except IntegrityError:
                db.session.rollback()
                print("failed")


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column( db.Integer, primary_key = True, autoincrement = True)
    name = db.Column( db.String(50), unique = True)
    description = db.Column( db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    recipes = db.relationship('Recipes', backref = 'category', lazy = 'dynamic')

    @staticmethod
    def data_generator(count=200):
        seed()
        num = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, num)).first()
            c = Categories(name=forgery_py.lorem_ipsum.word(),
            description=forgery_py.lorem_ipsum.sentence(),
            user= u)
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), unique = True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False )
    
    """ generates fake recipes for testing API """
    @staticmethod
    def data_generator(count=200):
        seed()
        user_num = User.query.count()
        cat_num = Categories.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_num-1)).first()
            c = Categories.query.offset(randint(0, cat_num-1)).first()
            r = Recipes(name = forgery_py.lorem_ipsum.word(),
            description = forgery_py.lorem_ipsum.sentence(),
            category = c, user = u)
            db.session.add(r)
        try:
            db.session.commit()
            print("successfully commited")
        except IntegrityError:
            db.session.rollback()
