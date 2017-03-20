from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


def create_test_user():
    """
    Creates a test user
    """
    User.objects.create_user(username='test', email='test@test.com', password='1111')


def create_test_budget(client):
    """
    Creates a test budget. Must be given a client, and a 'test'
    user must already exist
    :return: The response
    """
    user = User.objects.get(username='test')
    if user is None:
        raise Exception('Test user does not exist')
    client.force_login(user)

    response = client.post(reverse('budgetapp:budget-list'), {'month': 'JAN', 'year': 2017})
    if response.status_code != status.HTTP_201_CREATED:
        raise Exception('Test budget could not be created')

    client.logout()

    return response


class NoAuthenticationTests(APITestCase):
    """
    Ensures none of the actions (POST, PUT, LIST, DETAIL, DELETE) are allowed
    without authentication
    """

    def setUp(self):
        create_test_user()

    # --------------- BUDGET ------------------- #

    def test_list_budget(self):
        """
        LIST
        """
        response = self.client.get(reverse('budgetapp:budget-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_budget(self):
        """
        DETAIL
        """
        response = create_test_budget(self.client)
        response = self.client.get(response.data['url'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_budget(self):
        """
        POST
        """
        response = self.client.post(reverse('budgetapp:budget-list'), {'month': 'JAN', 'year': 2017})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_budget(self):
        """
        PUT
        """
        response = create_test_budget(self.client)
        response = self.client.put(response.data['url'], {'month': 'FEB'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_budget(self):
        """
        DELETE
        """
        response = create_test_budget(self.client)
        response = self.client.delete(response.data['url'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

