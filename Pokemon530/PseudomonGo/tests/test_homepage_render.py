from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from django.test import Client

class LoginRenderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com",username='testuser',password='12345')
        self.user.save()

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        self.assertEqual(logged_in, True)
        