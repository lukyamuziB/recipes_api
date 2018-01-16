from tests.basetest import BaseTestCase
import json

class TestUserAuth(BaseTestCase):

    def test_user_registration(self):
        user_data = {
            "name":"testname",
            "username":"testusername",
            "email":"nla@n.com",
            "password":"hbfhgsj"
        }
        response = self.app.post("/api/auth/register",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        print(msg)
        self.assertEqual(msg["Message"],"User Sucessfully Registered")
        self.assertEqual(response.status_code, 201)
    
    def test_user_cant_resgister_twice(self):
        user_data = {
            "name":"ben",
            "username":"lukya",
            "email":"lukyamuzibenon@gmail.com",
            "password":"1000kjkjkj"
        }
        response = self.app.post("/api/auth/register",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"User already exists")
        self.assertEqual(response.status_code, 409)
    
    def test_user_login(self):
        user_data = {
            
            "username":"lukya",
            "password":"1000"
        }
        response = self.app.post("/api/auth/login",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        print("kdsgfgausdgh")
        print(msg)
        self.assertEqual(msg["Message"],"Successfuly loged in")
        self.assertEqual(response.status_code, 200)
        

    def test_user_cant_login_with_unregistered_username(self):
        user_data = {
            
            "username":"lukyaqwerty",
            "password":"1000"
        }
        response = self.app.post("/api/auth/login",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Username is not Registered")
        self.assertEqual(response.status_code, 404)

    def test_user_cant_login_with_wrong_password(self):
        user_data = {
            
            "username":"lukya",
            "password":"10099we"
        }
        response = self.app.post("/api/auth/login",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Wrong Password")
        self.assertEqual(response.status_code, 404)
    
    def test_user_has_to_provide_password(self):
        """tests that a user can't attempt to login with empty password"""
        user_data = {
            
            "username":"lukya",
            "password":""
        }
        response = self.app.post("/api/auth/login",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Provide your password to login")
        self.assertEqual(response.status_code, 400)
    
    def test_user_has_to_provide_username(self):
        """tests that a user can't attempt to login with empty username"""
        user_data = {
            
            "username":"",
            "password":"1000uuuu"
        }
        response = self.app.post("/api/auth/login",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Provide your username to login")
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_email_format(self):
        user_data = {
            "name":"ben",
            "username":"lukya",
            "email":"lukya",
            "password":"1000kjkjkj"
        }
        response = self.app.post("/api/auth/register",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Enter your Email in the correct format")
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_username_format(self):
        user_data = {
            "name":"ben",
            "username":"__+&*&",
            "email":"lukya",
            "password":"1000kjkjkj"
        }
        response = self.app.post("/api/auth/register",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Make sure your username is only alphanumeric")
        self.assertEqual(response.status_code, 400)
    
    def test_short_password(self):
        user_data = {
            "name":"benon",
            "username":"lukyamuzi",
            "email":"lukya@gmail.com",
            "password":"10"
        }
        response = self.app.post("/api/auth/register",
         data=json.dumps(user_data), content_type="application/json")
        msg = json.loads(response.data)
        self.assertEqual(msg["Error"],"Make sure your password is at least 6 alphanumeric characters")
        self.assertEqual(response.status_code, 400)





        