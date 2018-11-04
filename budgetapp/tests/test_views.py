import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from ..views import ObtainAuthTokenCookieView, logout


class AuthViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username='test',
            password='test',
            email='test@test.com',
        )

    def test_obtain_auth_token_cookie_view(self):
        """
        Custom auth token view includes an http-only cookie with the token.
        """
        request = self.factory.post(reverse('budgetapp:obtain-auth-token'), {
            'username': 'test',
            'password': 'test',
        })
        response = ObtainAuthTokenCookieView.as_view()(request)
        cookie = response.cookies['Token']
        self.assertTrue(cookie.value)
        self.assertTrue(cookie['httponly'])
        self.assertEqual(json.loads(response.content), {
            'username': 'test',
            'email': 'test@test.com',
        })

    def test_logout(self):
        request = self.factory.get(reverse('budgetapp:logout'))
        response = logout(request)
        cookie = response.cookies['Token']
        self.assertEqual(cookie.value, 'logout')
        self.assertTrue(cookie['httponly'])
        self.assertEqual(cookie['expires'], 'Wed, 21 Oct 1900 07:28:00 GMT')
