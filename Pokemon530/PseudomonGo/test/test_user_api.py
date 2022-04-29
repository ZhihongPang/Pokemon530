from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

class UserAPITests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(email="test@test.com",username='testuser',password='12345')
        user.save()

    def test_registration(self):
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'password'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': '12345'
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_auth_user(self):
        # todo
        pass

    def test_logout(self):
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        