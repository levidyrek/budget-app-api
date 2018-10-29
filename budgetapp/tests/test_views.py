from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from ..views import ObtainAuthTokenCookieView


class AuthViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username='test',
            password='test',
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
        token = response.data['token']
        cookie = response.cookies['Token']
        self.assertEqual(cookie.value, token)
        self.assertTrue(cookie['httponly'])
