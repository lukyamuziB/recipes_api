#third party imports 
from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import ( get_jwt_identity,
    create_access_token, get_raw_jwt)

#local imports
from app.models import Categories, Recipes, User, Blacklist
from .. import jwt
from .. import db
from app.validators import (validate_username,
                   validate_email, validate_password)
from app.exceptions import (
    ResourceAlreadyExists, YouDontOwnResource,
    EmailEmpty, PasswordEmpty, UsernameEmpty, NameEmpty,
    EmptyField, EmptyDescription, WrongPassword,
    PasswordFormatError, EmailFormatError, UsernameFormatError
   )


def save(data):
    db.session.add(data)
    db.session.commit()


def belongs_to_user():
    """ picks currently logged in user id """
    usr_id = get_jwt_identity()
    return usr_id


def check_user_exists(username, email):
    if User.query.filter_by(username = username).first() or \
    User.query.filter_by(email = email).first():
        return False
    return True


def sanitize_edit_name(resource_instance, name):
    """takes in a name and makes sure its sanitized to catch ivalid 
       and empty inputs
    """
    if name is not None:
        if len(name) == 0:
            raise EmptyField
        else:
            resource_instance.name = name
    else:
         resource_instance.name = resource_instance.name
    

def sanitize_edit_description(resource_instance, description):
    """ takes in a description and makes sure its sanitized to catch invalid
        and empty inputs
    """
    if description is not None:
        if len(description) == 0:
            raise EmptyDescription
        else: 
            resource_instance.description = description
    else:
        resource_instance.description = resource_instance.description


def create_recipe(data, category_id, usr_id):
    """creates a recipe if doesn't exisr exists
       will throw a NoResult exception if the category you choose
       does not exist
    """
    name = data.get('name')
    description = data.get('description')
    category = Categories.query.filter_by(
        id =category_id, user_id = usr_id).first()
    if category is None:
        raise NoResultFound
    user = User.query.filter_by(id = usr_id).first()
    if not Recipes.query.filter_by(name = name, user_id = usr_id).first():
         recipe = Recipes(name = name, description = description,
         category = category, user = user)
         save(recipe)
    else:
        raise ResourceAlreadyExists


def update_recipe(recipe_id, data):
    """ updates a recipe if it exists """
    recipe = Recipes.query.filter(Recipes.id == recipe_id).first()
    if recipe is None:
        raise NoResultFound
    else:    
        name = data.get('name')
        description = data.get('description')
        sanitize_edit_name(recipe, name)
        sanitize_edit_description(recipe, description)
        recipe.modified = datetime.now()
        db.session.commit()


def delete_recipe(recipe_id, user_id):
    """ deletes a recipe if it exists """
    recipe = Recipes.query.filter_by(id = recipe_id,
                          user_id = user_id).first()
    if recipe is None:
        raise NoResultFound  
    else:
        db.session.delete(recipe)
        db.session.commit()


def create_category(data, user_id):
    """ creates a new category if it doesn't exist yet """
    name = data.get('name')
    description = data.get('description')
    user = User.query.filter_by(id = user_id).first()
    if not Categories.query.filter_by(name = name, user_id = user_id).first():
        category = Categories(name = name, 
        description = description, user = user)
        save(category)
    else:
        raise ResourceAlreadyExists


def update_category(category_id, data):
    """ updates a category a user made """
    category = Categories.query.filter_by(id = category_id).first()
    if category is None:
        raise NoResultFound
    else:
        description = data.get('description')
        name = data.get('name')
        sanitize_edit_name(category, name)
        sanitize_edit_description(category, description)
        category.modified = datetime.now()
        db.session.commit()


def delete_category(category_id, user_id):
    """ Deletes a category if it exists """
    category = Categories.query.filter_by(id = category_id, user_id = user_id ).first()
    if category is None:
        raise NoResultFound
    else:
        db.session.delete(category)
        db.session.commit()


def register_user(data):
    """ registers a non existent user """
    name = data.get('name').strip()
    username = data.get('username').strip()
    email = data.get('email').strip()
    password = data.get('password')
    if len(name) == 0:
        raise NameEmpty
    if len(username) == 0:
        raise UsernameEmpty
    else:
        if not validate_username(username):
            raise UsernameFormatError
    if len(password) == 0:
        raise PasswordEmpty
    else:
        if not validate_password(password):
            raise PasswordFormatError
    if len(email) == 0:
        raise EmailEmpty
    else:
        if not validate_email(email):
            raise EmailFormatError
    if check_user_exists(username, email):
        user = User(name = name, username = username,
                email = email, password = password )
        save(user)
    else:
        raise ResourceAlreadyExists


def user_login(data):
    """ logs in a registered user and creates a token """
    username = data.get('username')
    if len(username) == 0:
        raise UsernameEmpty
    password = data.get('password')
    user = User.query.filter_by(username = username).first()
    if user is None:
        raise NoResultFound
    elif len(password) == 0:
        raise PasswordEmpty
    else:
        #check user enters their password correctly
        if user.verify_password(password):
            access_token = create_access_token(identity = user.id,
                 expires_delta = timedelta(days=7))
            return access_token
        else:
            raise WrongPassword
    return access_token
    

def user_logout():
    """ blackklists a token """
    jti = get_raw_jwt()['jti']
    blacklist = Blacklist(token = jti)
    db.session.add(blacklist)
    db.session.commit()


def reset_password(data, id):
    """ resets a user's password """
    user = User.query.filter_by(id = id).first()
    old_password = data.get('old_password')
    if user.verify_password(old_password):
        new_password = data.get('new_password')
        user.password = password
    else:
        raise ValueError


def change_username(data, id):
    """ changes a user's username """
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
