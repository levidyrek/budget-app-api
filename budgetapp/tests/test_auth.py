from budgetapp.tests.utils import auth_util
from budgetapp.urls import app_name
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):

    def setUp(self):
        auth_util.create_test_users()
        self.setup_test_models(self.client)

    @staticmethod
    def setup_test_models(client):
        pass


class BudgetTests(BaseTestCase):
    """
    Ensures the actions (POST, PUT, LIST, DETAIL, DELETE) work as expected with
    and without authentication
    """

    model_name = auth_util.BUDGET_NAME

    # --------- No Authentication tests ---------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
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


class CategoryTests(BaseTestCase):

    model_name = auth_util.CATEGORY_NAME

    # --------- No authentication tests --------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
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


class CategoryBudgetGroupTests(BaseTestCase):

    model_name = auth_util.CATEGORYBUDGETGROUP_NAME

    @staticmethod
    def setup_test_models(client):
        # Test budget
        BudgetTests.setup_test_models(client)
        response = auth_util.create_test_model(client, auth_util.BUDGET_NAME)
        auth_util.post_data[auth_util.CATEGORYBUDGETGROUP_NAME]['budget'] = \
            response.data['url']

    # --------- No authentication tests --------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
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


class CategoryBudgetTests(BaseTestCase):

    model_name = auth_util.CATEGORY_NAME

    @staticmethod
    def setup_test_models(client):
        # Category
        CategoryTests.setup_test_models(client)
        response = auth_util.create_test_model(client, auth_util.CATEGORY_NAME)
        auth_util.post_data[auth_util.CATEGORYBUDGET_NAME]['category'] = \
            response.data['url']

        # CategoryBudgetGroup
        CategoryBudgetGroupTests.setup_test_models(client)
        response = auth_util.create_test_model(
            client, auth_util.CATEGORYBUDGETGROUP_NAME)
        auth_util.post_data[auth_util.CATEGORYBUDGET_NAME]['group'] = \
            response.data['url']

    # ------ No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
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


class TransactionTests(BaseTestCase):

    model_name = auth_util.TRANSACTION_NAME

    @staticmethod
    def setup_test_models(client):
        # Category Budget
        CategoryBudgetTests.setup_test_models(client)
        response = auth_util.create_test_model(
            client, auth_util.CATEGORYBUDGET_NAME)
        auth_util.post_data[auth_util.TRANSACTION_NAME]['category_budget'] = \
            response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Cross-User Actions ----------- #

    def test_detail_cross_user(self):
        response = auth_util.detail_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_cross_user(self):
        response = auth_util.put_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_cross_user(self):
        response = auth_util.delete_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class IncomeTests(BaseTestCase):

    model_name = auth_util.INCOME_NAME

    @staticmethod
    def setup_test_models(client):
        # Budget
        BudgetTests.setup_test_models(client)
        response = auth_util.create_test_model(client, auth_util.BUDGET_NAME)
        auth_util.post_data[auth_util.INCOME_NAME]['budget'] = \
            response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Cross-User Actions ----------- #

    def test_detail_cross_user(self):
        response = auth_util.detail_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_cross_user(self):
        response = auth_util.put_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_cross_user(self):
        response = auth_util.delete_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LongTermGoalTests(BaseTestCase):

    model_name = auth_util.LONGTERMGOAL_NAME

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Cross-User Actions ----------- #

    def test_detail_cross_user(self):
        response = auth_util.detail_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_cross_user(self):
        response = auth_util.put_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_cross_user(self):
        response = auth_util.delete_cross_user_test(
            self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BudgetGoalTests(BaseTestCase):

    model_name = auth_util.BUDGETGOAL_NAME

    @staticmethod
    def setup_test_models(client):
        # Long Term Goal
        LongTermGoalTests.setup_test_models(client)
        response = auth_util.create_test_model(
            client, auth_util.LONGTERMGOAL_NAME)
        auth_util.post_data[auth_util.BUDGETGOAL_NAME]['long_term_goal'] = \
            response.data['url']

        # Budget
        BudgetTests.setup_test_models(client)
        response = auth_util.create_test_model(client, auth_util.BUDGET_NAME)
        auth_util.post_data[auth_util.BUDGETGOAL_NAME]['budget'] = \
            response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = auth_util.post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = auth_util.put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, True)
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


class UserTests(BaseTestCase):

    model_name = auth_util.USER_NAME
    detail_url = None
    detail_url2 = None

    def setUp(self):
        super(UserTests, self).setUp()

        test_pk = User.objects.get(
            username=auth_util.test_users[0]['username']
        ).pk
        self.detail_url = reverse(app_name + ':' + self.model_name + '-detail',
                                  args=[test_pk])

        test_pk = User.objects.get(
            username=auth_util.test_users[1]['username']
        ).pk
        self.detail_url2 = reverse(
            app_name + ':' + self.model_name + '-detail',
            args=[test_pk]
        )

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        Note: Should succeed without authentication
        """
        url = app_name + ':' + self.model_name + '-create'
        response = self.client.post(
            reverse(url), auth_util.post_data[self.model_name]
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_no_auth(self):
        response = self.client.put(self.detail_url, )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------- Authentication tests -------- #

    def test_list_auth(self):
        """
        Forbidden for non-admin users
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
        auth_util.login_test_user(self.client, 0)
        response = self.client.get(self.detail_url2)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_cross_user(self):
        auth_util.login_test_user(self.client, 0)
        response = self.client.put(
            self.detail_url2, auth_util.post_data[auth_util.USER_NAME])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cross_user(self):
        auth_util.login_test_user(self.client, 0)
        response = self.client.delete(self.detail_url2)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
