from budgetapp.tests.utils import auth_util
from budgetapp.urls import app_name
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BaseTestMixin:
    """
    Ensures the actions (POST, PUT, LIST, DETAIL, DELETE) work as expected with
    and without authentication
    """

    def setUp(self):
        auth_util.create_test_users()
        self.setup_test_models(self.client)

    @staticmethod
    def setup_test_models(client):
        pass

    # --------- No Authentication tests ---------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = \
            auth_util.list_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = \
            auth_util.detail_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = \
            auth_util.post_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = \
            auth_util.put_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = \
            auth_util.delete_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Cross-User Actions ----------- #

    def test_detail_cross_user(self):
        response = auth_util.detail_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_cross_user(self):
        response = auth_util.put_cross_user_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_cross_user(self):
        response = auth_util.delete_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BudgetTests(BaseTestMixin, APITestCase):
    model_name = auth_util.BUDGET_NAME


class CategoryTests(BaseTestMixin, APITestCase):
    model_name = auth_util.CATEGORY_NAME


class CategoryBudgetGroupTests(BaseTestMixin, APITestCase):
    model_name = auth_util.CATEGORYBUDGETGROUP_NAME

    @staticmethod
    def setup_test_models(client):
        # Test budget
        BudgetTests.setup_test_models(client)
        response = auth_util.create_test_model(client, auth_util.BUDGET_NAME)
        auth_util.post_data[auth_util.CATEGORYBUDGETGROUP_NAME]['budget'] = \
            response.data['url']


class UserTests(BaseTestMixin, APITestCase):
    model_name = auth_util.USER_NAME

    def setUp(self):
        super(UserTests, self).setUp()

        test_pk = User.objects.get(
            username=auth_util.test_users[0]['username']
        ).pk
        self.detail_url = \
            auth_util.get_url(self.model_name, 'detail', args=[test_pk])

        test_pk = User.objects.get(
            username=auth_util.test_users[1]['username']
        ).pk
        self.detail_url2 = \
            auth_util.get_url(self.model_name, 'detail', args=[test_pk])

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_no_auth(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_no_auth(self):
        """
        Users can be created without authentication.
        """
        url = auth_util.get_url(self.model_name, 'create')
        response = self.client.post(url, auth_util.post_data[self.model_name])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_no_auth(self):
        response = self.client.put(
            self.detail_url, auth_util.post_data[auth_util.USER_NAME])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_no_auth(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------- Authentication tests -------- #

    def test_list_auth(self):
        """
        Forbidden for non-admin users.
        """
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_auth(self):
        auth_util.login_test_user(self.client)
        response = self.client.get(self.detail_url)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        auth_util.login_test_user(self.client)
        url = app_name + ':' + self.model_name + '-create'
        response = self.client.post(
            reverse(url), auth_util.post_data[self.model_name])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        auth_util.login_test_user(self.client)
        response = self.client.put(
            self.detail_url, auth_util.post_data[auth_util.USER_NAME])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        auth_util.login_test_user(self.client)
        response = self.client.delete(self.detail_url)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Cross-User Actions ----------- #

    def test_detail_cross_user(self):
        auth_util.login_test_user(self.client, index=0)
        response = self.client.get(self.detail_url2)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_cross_user(self):
        auth_util.login_test_user(self.client, index=0)
        response = self.client.put(
            self.detail_url2, auth_util.post_data[auth_util.USER_NAME])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cross_user(self):
        auth_util.login_test_user(self.client, index=0)
        response = self.client.delete(self.detail_url2)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
