from app.models import Categories, Recipes
from ... import db


def create_recipe(data):
    name = data.get('name')
    description = data.get('description')
    category_id = data.get('category_id')
    recipe_id = data.get('recipe_id')
    category = Categories.query.filter(Categories.id == category_id).one()
    recipe = Categories(name, description)
    db.session.add(recipe)
    db.session.commit()


def update_recipe(recipe_id, data):
    post = Recipes.query.filter(Recipes.id == recipe_id).one()
    post.title = data.get('title')
    post.body = data.get('body')
    category_id = data.get('category_id')
    post.category = Categories.query.filter(Categories.id == category_id).one()
    db.session.add(post)
    db.session.commit()


def delete_recipe(recipe_id):
    recipe = Recipes.query.filter(Recipes.id == recipe_id).one()
    db.session.delete(recipe)
    db.session.commit()


def create_category(data):
    category_id = data.get('id')
    name = data.get('name')
    description = data.get('description')

    category = Category(name)
    if category_id:
        category.id = category_id

    db.session.add(category)
    db.session.commit()


def update_category(category_id, data):
    category = Category.query.filter(Category.id == category_id).one()
    category.name = data.get('name')
    db.session.add(category)
    db.session.commit()


def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id).one()
    db.session.delete(category)
    db.session.commit()
