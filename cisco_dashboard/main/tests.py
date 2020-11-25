from django.test import TestCase
#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
# Create your tests here.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(True)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
    def test_mainpage(self):
        print('test mainpage status code')
        response=self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_page(self):
        print('test mysub status code')
        response=self.client.get('/ruofan')
        self.assertEqual(response.status_code, 200)
