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
            "password":"1000"
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
    
    # def test_user_can_log_out(self):
    #     response = self.app.delete("/api/auth/logout")
    #     msg = json.loads(response.data)
    #     self.assertEqual(msg["Message"],"Successfully loged out")
    #     self.assertEqual(response.status_code, 200)



