from app.models import Categories, Recipes, User
from ... import db


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
        return True
    return False


def create_recipe(data, category_id, usr_id):
    name = data.get('name')
    description = data.get('description')
    category = Categories.query.filter_by(id =category_id).first()
    user = User.query.filter_by(id = usr_id).first()
    if check_recipe_exists(name):
         recipe = Recipes(name = name, description = description,
         category = category, user = user)
         save(recipe)
    else:
        return 0


def update_recipe(recipe_id, data):
    recipe = Recipes.query.filter(Recipes.id == recipe_id).first()
    recipe.name = data.get('name')
    recipe.description = data.get('description')
    db.session.commit()


def delete_recipe(recipe_id):
    recipe = Recipes.query.filter(Recipes.id == recipe_id).one()
    save(recipe)


def create_category(data, user_id):
    name = data.get('name')
    description = data.get('description')
    user = User.query.filter_by(id = user_id).first()
    if check_category_exists(name):
        category = Categories(name = name, 
        description = description, user = user)
        save(category)


def update_category(category_id, data):
    category = Categories.query.filter_by(id = category_id).first()
    category.name = data.get('name')
    category.description = data.get('description')
    db.session.add(category)
    db.session.commit()


def delete_category(category_id):
    category = Categories.query.filter_by(id = category_id).first()
    db.session.delete(category)
    db.session.commit()


def register_user(data):
    name = data.get('name')
    username = data.get('username')
    email = date.get('email')
    password = date.get('password')
    user = User(name = name, username = username, email = email, password = password )
    db.session.add()


def user_login(data):
    pass


def user_logout():
    pass



