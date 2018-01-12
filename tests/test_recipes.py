from tests.basetest import BaseTestCase
import json
from app.models import User,Categories
from app import db
from sqlalchemy.exc import IntegrityError
import pytest

class TestRecipes(BaseTestCase):
    def setUp(self):
        super(TestRecipes, self).setUp()
        a = User(name = "someguy", username = "guy",
                password = "7910", email="blah")
        try:
            db.session.add(a)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        auth_request = self.app.post('/api/auth/login',
                                           data=json.dumps(
                                               {'username': 'guy', 'password': '7910'}),
                                           headers={'Content-Type': 'application/json'})
        auth_token = json.loads(auth_request.data)['token']
        self.access_token = '{0}'.format(auth_token)
            
    def test_get_recipe_with_no_auth(self):
        """Tests for getting recipes without authentication"""
        resp = self.app.get('api/recipes/2')
        self.assertEqual(resp.status_code, 200)
    
    def test_create_recipe(self):
        """Tests for creation of a recipe"""

        usr_data = {
            "name":"samplerecipe",
            "description":"sampledescription",
            "category_id":1
        }        
        
        response = self.app.post(
                    "/api/recipes", data=json.dumps(usr_data), headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})      
        self.assertEqual(response.status_code, 201)
    
    # @pytest.mark.skip
    def test_cant_create_recipe_twice(self):
        usr_data = {
            "name":"sample",
            "description":"sample",
            "category_id":1
        }        
        
        response = self.app.post(
                    "/api/recipes", data=json.dumps(usr_data), headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})
        msg = json.loads(response.data)             
        self.assertEqual(response.status_code, 409)
        self.assertEqual(msg['Error'], "You are creating an already existent Recipe")
    
    def test_recipe_cant_belong_to_no_category(self):
        usr_data = {
            "name":"sample23",
            "description":"sample",
            "category_id":9090
        }        
        
        response = self.app.post(
                    "/api/recipes", data=json.dumps(usr_data), headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(msg['Error'], "Recipe can't belong to non existent Category")
    
    def test_user_cant_edit_recipe_they_didnt_create(self):
        usr_data = {
            "name":"newnmame",
            "description":"newdescription"
        }
        response = self.app.put(
                    "/api/recipes/1", data=json.dumps(usr_data), headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(msg['Error'], "Can't edit a recipe you didnt create")
    
    def test_user_cant_edit_recipe_that_doesnt_exist(self):
        usr_data = {
            "name":"newnmame",
            "description":"newdescription"
        }
        response = self.app.put(
                    "/api/recipes/1000", data=json.dumps(usr_data), headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(msg['Error'], "Can't edit non existent recipe")

    def test_cant_delete_a_recipe_user_didnt_create(self):
        response = self.app.delete(
                    "/api/recipes/1", headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(msg['Error'], "Can't delete a recipe you didnt create")
    
    def test_cant_delete_a_recipe_that_doesnt_exist(self):
        response = self.app.delete(
                    "/api/recipes/1000", headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 404)















