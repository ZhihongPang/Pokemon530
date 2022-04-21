from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

class UserAPITests(APITestCase):

    def setup(self):
        self.user = User.objects.create(email="test@test.com",username='testuser', password='12345')

    def test_registration(self):
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'password'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        