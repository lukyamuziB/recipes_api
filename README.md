# Yummy Recipes Api
[![Build Status](https://travis-ci.org/lukyamuziB/recipes_api.svg?branch=master)](https://travis-ci.org/lukyamuziB/recipes_api)
[![Coverage Status](https://coveralls.io/repos/github/lukyamuziB/recipes_api/badge.svg?branch=master)](https://coveralls.io/github/lukyamuziB/recipes_api?branch=master)
<a href="https://www.python.org/dev/peps/pep-0008/">
<img class="notice-badge" src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="Badge"/>
</a>

# RecipeAPI

This is an API for a Recipes service using Flask. Users can register an account and login to create, edit, view and delete recipe categories and recipes in those categories.

Sample documents is as bellow, A deatiled interactive documentation provided by swaggher is at your base URL
locally it will be at;

   ```
   http://127.0.0.0.1/5000/api
   ```
Note that your port number may differ

| EndPoint                                   | Functionality                                    |
| ------------------------------------------ | ------------------------------------------------ |
| [ POST /auth/login/ ](#)                   | Logs a user in                                   |
| [ POST /auth/register/ ](#)                | Register a user                                  |
| [ DELETE /auth/logout/ ](#)                | Logout a user                                    |
| [ POST /categories/ ](#)                   | Create a new category                            |
| [ GET /categories/ ](#)                    | Get all categories                               |
| [ GET /categories/\<id>/ ](#)              | Get a category by it's id                        |
| [ PUT /categories/\<id>/ ](#)              | Update the category                              |
| [ DELETE /categories/\<id>/ ](#)           | Delete the category                              |
| [ POST /recipes ](#)                       | Create a recipe in the specified category        |
| [ GET /recipes/](#)                        | Get all recipes created by the logged in user    |
| [ GET /recipes/\<id>/](#)                  | Get all recipes in the specified category id     |
| [ GET /recipes/\<id>/](#)    | Get a recipe in the specified category id        |
| [ PUT /recipes/\<id>/](#)    | Update the recipe in the specified category id   |
| [ DELETE /recipes/<id>/(#)                | Delete the recipe in the specified category id   |

## Setup

To use the application, ensure that you have python 3.6+, clone the repository to your local machine. Open your git commandline and run

1. Clone the repository

   ```
   git clone https://github.com/Thegaijin/recipeAPI.git
   ```

2. Enter the project directory
   ```
   cd recipeAPI
   ```
3. Create a virtual environment
   ```
   virtualenv venv
   ```
4. Activate the virtual environment
   ```
   source venv/bin/activate
   ```
5. Then install all the required dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Install postgres if you don't already have it. Preferably Postgres 10.1.

7. Create the Databases

   #### For the test Database

   ```
   createdb api
   ```

   #### For the development Database

   ```
   createdb test_api
   ```

8. Run Migrations using these commands, in that order:

   ```
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

9. To test the application, run the command :

   ```
   python manage.py test
   ```

10. To start the server, run the command:
    ```
    python manage.py runserver
    ```
