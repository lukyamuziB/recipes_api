from tests.basetest import BaseTestCase
import json
from app.models import User,Categories, Recipes
from app import db
from sqlalchemy.exc import IntegrityError
import pytest

class TestCategories(BaseTestCase):
    def setUp(self):
        super(TestCategories, self).setUp()
        user = User(name = "someguy", username = "guy",
                password = "7910", email="blah@blah.com")
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        auth_request = self.app.post('/api/auth/login',
                            data=json.dumps(
                            {'username': 'guy', 'password': '7910'}),
                            headers={'Content-Type': 'application/json'})
        auth_token = json.loads(auth_request.data)['token']
        self.access_token = '{0}'.format(auth_token)
        category = Categories(name="samplecat", 
        description="sampledesc", user = user)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


    def test_cant_get_categories_with_no_auth(self):
        resp = self.app.get('api/categories')
        self.assertEqual(resp.status_code, 401)
    
    def test_can_create_category(self):
        usr_data = {
            "name":"samplerecipe",
            "description":"sampledescription"
        }        
        
        response = self.app.post(
                    "/api/categories", data=json.dumps(usr_data),
                     headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})      
        self.assertEqual(response.status_code, 201)

    def test_cant_create_category_twice(self):
        usr_data = {
            "name":"samplecat",
            "description":"sampledesc"
        }        

        response = self.app.post(
                    "/api/categories", data=json.dumps(usr_data),
                     headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})  
        msg = json.loads(response.data)     
        self.assertEqual(response.status_code, 409)
        self.assertEqual(msg['Error'], 
        "You are creating an already existent Category")

    
    def test_can_edit_category(self):
        cat = Categories.query.filter_by(name = 'samplecat').first()
        usr_data ={
            "name":"newname",
            "description":"newdescriotion"
        }
        response = self.app.put(
                    "/api/categories/2", data=json.dumps(usr_data),
                     headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})      
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(msg['Message'], "Category successfully updated")
    
    def test_cant_edit_non_existent_category(self):
        """tests that  user can't create a category twice"""
        usr_data ={
            "name":"samplecate",
            "description":"sampledesc"
        }
        response = self.app.put(
                    "/api/categories/1000", data=json.dumps(usr_data),
                     headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})      
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(msg['Error'], "Can't edit non existent Category")

    
    def test_can_delete_category(self):
        """tests user can delete category"""
        response = self.app.delete(
                    "/api/categories/2", 
                    headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})      
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(msg['Message'], "Successfully Deleted Category")
    
    def test_cant_delete_non_existent_category(self):
        """test you cant non existent category"""
        response = self.app.delete(
                    "/api/categories/1000", 
                    headers={'Content-Type': 'application/json',
                     'Authorization': "Bearer " + self.access_token})      
        msg = json.loads(response.data)        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(msg['Error'], "Can't delete non existent Category")


        