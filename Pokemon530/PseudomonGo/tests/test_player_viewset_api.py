from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from PseudomonGo.models import Player
from rest_framework.permissions import AllowAny, IsAuthenticated

class PlayerViewsetTests(APITestCase):
    
    def setUp(self):
        pass
    
    def test_get_without_auth(self):
        response = self.client.get('/api/players/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_with_auth(self):
        pass
