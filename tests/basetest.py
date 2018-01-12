from flask_testing import TestCase
from config import TestingConfig
from app import create_app, db
from sqlalchemy.exc import IntegrityError
from app.models import User, Categories, Recipes


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(TestingConfig) 
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.create_all()
        user = User(name = "ben", username = "lukya", 
                    email = "lukyamuzibenon@gmail.com", password = "1000")
        ctg = Categories(name = "sample", description = "sample", user = user)
        recipe = Recipes(name="sample", description="sample", category=ctg, user=user)
        try:
            db.session.add_all([user,ctg,recipe])
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
