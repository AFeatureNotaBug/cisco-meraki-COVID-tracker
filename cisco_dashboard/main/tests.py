"""Django Unit Tests"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

# Create your tests here.
class Register(TestCase):
    """Tests Register"""
    def test_register(self):
        """Tests register"""
        # send register data
        #response = self.client.post('/register/', self.credentials, follow=True)
        body = {'username':'aa',
            'email':'549956326@qq.com',
            'password':'secret',
            'apikey':'customerday1'
        }
        self.client.post('/register/', body, follow=True)
        # should be logged in now
        print('hello register')
#        self.assertTrue(response.context['username'].is_active)

class LogInTest(TestCase):
    """Tests login"""
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        """Test login"""
        # send login data
        x = self.client.post('/login/', self.credentials, follow=True)
        print(x)
        # should be logged in now
        print('hello login')
#        self.assertTrue(response.context['username'].is_active)
class YourTestClass(TestCase):
    """Your Test Class"""
    @classmethod
    def setUpTestData(cls):
        """Set up test dataa"""
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

class RegisterLoginTest(TestCase):
    """Tests registration and login functionality"""
    def test_register_and_login(self):
        """
         * Test registration functionality by registering a test account
         * Also test login functionality by logging in to the registered user account
        """
        user_creds = {
            'username':'aa',
            'email':'549956326@qq.com',
            'password':'secret',
            'apikey':'customerday1'
        }

        response = self.client.post(
            '/register/',
            user_creds,
            follow = True
        )

        self.assertTrue(response.status_code == 200)    # Check registration was successful
        assert User.objects.get(username = "aa")        # Ensure user exists

class ChangeAPIKeyTest(TestCase):
    def test_change_api_key(self):
        testdata = {
            'username':'testuseralpha',
            'email':'testuser@test.com',
            'password':'testuser',
            'apikey':'testcase1'
        }

        self.credentials = {
            'username': 'testuseralpha',
            'password': 'testuser'}

        self.client.post('/register/', testdata, follow=True)
        self.client.login(username=testdata['username'],password=testdata['password'])
        testdatabeta = {'apikey':'testcase2'}
        self.client.post('/editapikey', testdatabeta, follow=True)
        user = User.objects.get(username=testdata['username'])
        userprofile = UserProfile.objects.get(user = user)
        assert (userprofile.apikey == testdatabeta['apikey'])

class LogOutTest(TestCase):
    def test_logout(self):
        self.credentials = {
            'username': 'testuserbeta',
            'email':'testuser@test.com',
            'password': 'secret',
            'apikey':'testcase1'
            }
        self.client.post('/register/', self.credentials, follow=True)
        #Login first so the option to logout is availible
        self.client.login(username=self.credentials['username'],password=self.credentials['password'])
        response = self.client.post('/logout/', self.credentials, follow=True)
        print(response.status_code)
        self.assertTrue(response.status_code == 200)

class UseDemoKeyTest(TestCase):
    def test_demo_key(self):
        testprofile = {
            'username': 'testuser',
            'email':'testuser@test.com',
            'password': 'secret',
            'apikey':'testcase1'
            }
        self.client.post('/register/', testprofile, follow=True)
        self.client.login(username=testprofile['username'],password=testprofile['password'])
        req = self.client.post('/usedemokey', follow=True)
        user = User.objects.get(username=testprofile['username'])
        userprofile = UserProfile.objects.get(user = user)
        testdatabeta = {'apikey':'demo'}
        self.assertEqual(userprofile.apikey, testdatabeta['apikey'])
        