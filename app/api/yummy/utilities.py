from app.models import Categories, Recipes, User, Blacklist
from ... import jwt
from ... import db
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import ( get_jwt_identity,
    create_access_token, get_raw_jwt)
from datetime import datetime, timedelta
from flask import jsonify


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


#picks user id from the token
def belongs_to_user():
    usr_id = get_jwt_identity()
    return usr_id


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
    elif belongs_to_user() != recipe.user.id:
        raise TypeError
    else:    
        name = data.get('name')
        recipe.name = name if name is not None else recipe.name
        description = data.get('description')
        recipe.description = description if description is not None else recipe.description
        recipe.modified = datetime.now()
        db.session.commit()


#deletes a recipe if it exists
def delete_recipe(recipe_id):
    recipe = Recipes.query.filter_by(id = recipe_id).first()
    if recipe is None:
        raise ValueError
    elif belongs_to_user != recipe.user.id:
        raise TypeError    
    else:
        db.session.delete(recipe)
        db.session.commit()


#creates a new category if it doesn't exist yet
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
    elif belongs_to_user() != category.user.id:
        raise TypeError 
    else:
        name = data.get('name')
        category.name = name if name is not None else category.name
        description = data.get('description')
        category.description = description if description is not None else category.description
        category.modified = datetime.now()
        db.session.commit()


#Deletes a category if it exists
def delete_category(category_id):
    category = Categories.query.filter_by(id = category_id).first()
    if category is None:
        raise ValueError
    elif belongs_to_user != category.user.id:
        raise TypeError 
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
        save(user)
    else:
        raise ValueError


#logs in a registered user and creates a token
def user_login(data):
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username = username).first()
    if user is None:
        raise NoResultFound
    else:
        if user.verify_password(password):
            access_token = create_access_token(identity = user.id, expires_delta = timedelta(days=7))
            return access_token
        else:
            raise ValueError
    return access_token
    

#blackklists a token
def user_logout():
    jti = get_raw_jwt()['jti']
    blacklist = Blacklist(token = jti)
    db.session.add(blacklist)
    db.session.commit()


#resets a user's password
def reset_password(data, id):
    user = User.query.filter_by(id = id).first()
    password = data.get('password')
    user.password = password


#changes a user's username
def change_username(date, id):
    user = User.query.filter_by(id = id).first()
    username = data.get('username')
    user.username = username


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """ Call back function that checks if a the token is valid on all the
        endpoints that require a token
    """
    jti = decrypted_token['jti']

    if Blacklist.query.filter_by(token=jti).first() is None:
        return False
    return True


@jwt.revoked_token_loader
def my_revoked_token_callback():
    return jsonify({'message': 'You must be logged in to access this page'})