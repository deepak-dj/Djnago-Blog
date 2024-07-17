from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from tests.factory import UserFactory
from unittest.mock import patch, MagicMock


class TestUserRegister(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user.set_password('securepassword')
        self.user.save()
        # self.mock_user = {"email": "xyz@g.com", "password": "passwd"}

    def test_register_user(self):
        url = reverse("register-list")
        payload = {
            "username": "ab",
            "email": "ab@y.com",
            "password": "password"
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'username': 'ab', 'email': 'ab@y.com'})

    @patch('django.contrib.auth.authenticate')
    @patch("blog_app.views.RefreshToken.for_user")
    def test_login_user_with_valid_credentials(self, mock_for_user, mock_authenticate):
        mock_authenticate.return_value = self.user
        mock_refresh_token = MagicMock()
        mock_refresh_token.access_token = 'mock_access_token'
        mock_refresh_token.__str__.return_value = 'mock_refresh_token'

        mock_for_user.return_value = mock_refresh_token

        url = reverse("login")
        payload = {
            "email": self.user.email,
            "password": "securepassword"
        }

        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, {'access': 'mock_access_token', 'refresh': 'mock_refresh_token'}
                         )

    def test_login_user_without_credentials(self):
        url = reverse("login")
        payload = {
            "email": self.user.username,
            "password": self.user.password
        }

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'detail': 'Invalid credentials'})
