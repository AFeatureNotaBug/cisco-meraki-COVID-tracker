"""Django Unit Tests"""
import meraki
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from main.models import Organisation
#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing


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

        user = authenticate(username='aa', password='secret')         # Login with register details
        self.assertTrue((user is not None) and user.is_authenticated) # Assert login was successful


class TestAPI(TestCase):
    """Simple API Test.
     *  Retrieves DevNet Sandbox organisation using the test API key
     *  Creates a db object for the organisation
     *  Checks that creation was successful
    """

    def test_api_call_and_model(self):
        """
         * This function retrieves the DevNet Sandbox organisation and stores it in the db
         * The organisation will then be retrieved and checked
        """
        api_key = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"    # Test API keys
        dash = meraki.DashboardAPI(api_key) # Set up dash using API keys

        try:
            devnet = dash.organizations.getOrganization("549236")

            test_org = Organisation.objects.create(
                orgID   = devnet['id'],
                orgName = devnet['name'],
                orgURL  = devnet['url'],
                apikey = api_key
            )
            test_org.save()

        except meraki.exceptions.APIError:
            assert False


        try:
            get_org = Organisation.objects.get(orgID = "549236")
            self.assertEqual(get_org, test_org)

        except Organisation.DoesNotExist:
            assert False
