from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class UserAPITests(APITestCase):

    def test_registration(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testcase',
            'password': 'pass',
            'user_permissions': []
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)