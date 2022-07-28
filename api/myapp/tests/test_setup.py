from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url=reverse('register')

        self.user_data = {
            'username': "karan", 
            'password': "emailpass",
            'email': "karan@gmail.com",
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
