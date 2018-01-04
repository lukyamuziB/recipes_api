from app.models import Categories, Recipes, User
from ... import db
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import create_access_token
from datetime import datetime


def save(data):
    db.session.add(data)
    db.session.commit()


def check_category_exists(category):
    ctg = Categories.query.filter_by(name = category).first()
    if ctg:
        return False
    return True


def check_recipe_exists(recipe):
    rcp = Recipes.query.filter_by(name = recipe).first()
    if rcp:
        return False
    return True


def check_user_exists(username, email):
    if User.query.filter_by(username = username).first() or \
    User.query.filter_by(email = email).first():
        return False
    return True


#creates a recipe if it exists
def create_recipe(data, category_id, usr_id):
    name = data.get('name')
    description = data.get('description')
    category = Categories.query.filter_by(id =category_id).first()
    if category is None:
        raise NoResultFound
    user = User.query.filter_by(id = usr_id).first()
    if check_recipe_exists(name) and category is not None:
         recipe = Recipes(name = name, description = description,
         category = category, user = user)
         save(recipe)
    else:
        raise ValueError


#updates a recipe if it exists
def update_recipe(recipe_id, data):
    recipe = Recipes.query.filter(Recipes.id == recipe_id).first()
    if recipe is None:
        raise ValueError
    else:    
        name = data.get('name')
        recipe.name = name if name is not None else recipe.name
        description = data.get('description')
        recipe.description = description if description is not None else recipe.description
        # recipe.modified = datetime.utcnow
        db.session.commit()


#deletes a recipe if it exists
def delete_recipe(recipe_id):
    recipe = Recipes.query.filter_by(id = recipe_id).first()
    if recipe is None:
        raise ValueError
    else:
        db.session.delete(recipe)
        db.session.commit()


#creates a new category or raises  a value error if category already exists
def create_category(data, user_id):
    name = data.get('name')
    description = data.get('description')
    user = User.query.filter_by(id = user_id).first()
    if check_category_exists(name):
        category = Categories(name = name, 
        description = description, user = user)
        save(category)
    else:
        raise ValueError


#updates a category a user made
def update_category(category_id, data):
    category = Categories.query.filter_by(id = category_id).first()
    if category is None:
        raise ValueError
    else:
        name = data.get('name')
        category.name = name if name is not None else category.name
        description = data.get('description')
        category.description = description if description is not None else category.description
        # recipe.modified = datetime.utcnow
        db.session.commit()


#Deletes a category if it exists
def delete_category(category_id):
    category = Categories.query.filter_by(id = category_id).first()
    if category is None:
        raise ValueError
    else:
        db.session.delete(category)
        db.session.commit()


#registers a non existent user
def register_user(data):
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if check_user_exists(username, email):
        user = User(name = name, username = username, email = email, password = password )
        db.session.add(user)
        db.session.commit()
    else:
        raise ValueError


def user_login(data):
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username = username).first()
    if user is None:
        raise NoResultFound
    else:
        if user.verify_password(password):
            access_token = create_access_token(identity = user.id)
            return access_token
        else:
            raise ValueError
    return access_token
    
        

    
    


def user_logout():
    pass
