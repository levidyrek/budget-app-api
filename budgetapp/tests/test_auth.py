from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from ..urls import app_name
from datetime import date


# Model Names
BUDGET_NAME = 'budget'
CATEGORY_NAME = 'category'
CATEGORYBUDGETGROUP_NAME = 'categorybudgetgroup'
CATEGORYBUDGET_NAME = 'categorybudget'
TRANSACTION_NAME = 'transaction'
INCOME_NAME = 'income'
LONGTERMGOAL_NAME = 'longtermgoal'
BUDGETGOAL_NAME = 'budgetgoal'

# Test Data
post_data = {
    BUDGET_NAME: {'month': 'JAN', 'year': 2017},
    CATEGORY_NAME: {'name': 'Groceries'},
    CATEGORYBUDGETGROUP_NAME: {'name': 'test', 'budget': ''},
    CATEGORYBUDGET_NAME: {'limit': 100, 'spent': 0, 'group': '', 'category': ''},
    TRANSACTION_NAME: {'amount': 100, 'recipient': 'test', 'category_budget': '',
                       'date': date.today()},
    INCOME_NAME: {'amount': 100, 'name': 'paycheck 1', 'budget': ''},
    LONGTERMGOAL_NAME: {'name': 'test', 'goal_amount': 100, 'progress': 0,
                        'due_date': date.today()},
    BUDGETGOAL_NAME: {'name': 'test', 'goal_amount': 100, 'progress': 0,
                      'long_term_goal': '', 'budget': ''},
}
put_data = {
    BUDGET_NAME: {'month': 'FEB', 'year': 2018},
    CATEGORY_NAME: {'name': 'Dining Out'},
    CATEGORYBUDGETGROUP_NAME: {'name': 'test2'},
    CATEGORYBUDGET_NAME: {'limit': 200, 'spent': 100},
    TRANSACTION_NAME: {'amount': 200},
    INCOME_NAME: {'amount': 200},
    LONGTERMGOAL_NAME: {'name': 'test2'},
    BUDGETGOAL_NAME: {'name': 'test2'},
}


# ------- Helper Functions ------- #


def create_test_user():
    """
    Creates a test user
    """
    User.objects.create_user(username='test', email='test@test.com', password='1111')


def create_test_model(client, model_name):
    """
    Logs in as test user (create_test_user must be called first) and
    calls the test model function corresponding to the given name
    :param client: 
    :param model_name: Name of the model to be created
    :return: The post response
    """
    user = User.objects.get(username='test')
    if user is None:
        raise Exception('Test user does not exist')
    client.force_login(user)

    url = app_name + ':' + model_name + '-list'
    test_data = post_data[model_name]

    response = client.post(reverse(url), test_data)
    if response.status_code != status.HTTP_201_CREATED:
        raise Exception('Test ' + model_name + ' could not be created: ' +
                        str(response.data))

    client.logout()

    return response


def list_test(client, model_name):
    url = app_name + ':' + model_name + '-list'
    return client.get(reverse(url))


def post_test(client, model_name):
    url = app_name + ':' + model_name + '-list'
    return client.post(reverse(url), post_data[model_name])


def detail_test(client, model_name):
    response = create_test_model(client, model_name)
    return client.get(response.data['url'])


def put_test(client, model_name):
    response = create_test_model(client, model_name)
    return client.put(response.data['url'], put_data[model_name])


def delete_test(client, model_name):
    response = create_test_model(client, model_name)
    return client.delete(response.data['url'])


class BaseTestCase(APITestCase):

    def setUp(self):
        create_test_user()
        self.setup_test_models(self.client)

    @staticmethod
    def setup_test_models(client):
        pass


class BudgetTests(BaseTestCase):
    """
    Ensures none of the actions (POST, PUT, LIST, DETAIL, DELETE) are allowed
    without authentication
    """

    # --------- No Authentication tests ---------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryTests(BaseTestCase):

    # --------- No authentication tests --------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryBudgetGroupTests(BaseTestCase):

    @staticmethod
    def setup_test_models(client):
        # Test budget
        BudgetTests.setup_test_models(client)
        response = create_test_model(client, BUDGET_NAME)
        post_data[CATEGORYBUDGETGROUP_NAME]['budget'] = response.data['url']

    # --------- No authentication tests --------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryBudgetTests(BaseTestCase):

    @staticmethod
    def setup_test_models(client):
        # Category
        CategoryTests.setup_test_models(client)
        response = create_test_model(client, CATEGORY_NAME)
        post_data[CATEGORYBUDGET_NAME]['category'] = response.data['url']

        # CategoryBudgetGroup
        CategoryBudgetGroupTests.setup_test_models(client)
        response = create_test_model(client, CATEGORYBUDGETGROUP_NAME)
        post_data[CATEGORYBUDGET_NAME]['group'] = response.data['url']

    # ------ No authentication tests -------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TransactionTests(BaseTestCase):

    @staticmethod
    def setup_test_models(client):
        # Category Budget
        CategoryBudgetTests.setup_test_models(client)
        response = create_test_model(client, CATEGORYBUDGET_NAME)
        post_data[TRANSACTION_NAME]['category_budget'] = response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, TRANSACTION_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, TRANSACTION_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, TRANSACTION_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, TRANSACTION_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, TRANSACTION_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IncomeTests(BaseTestCase):

    @staticmethod
    def setup_test_models(client):
        # Budget
        BudgetTests.setup_test_models(client)
        response = create_test_model(client, BUDGET_NAME)
        post_data[INCOME_NAME]['budget'] = response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, INCOME_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, INCOME_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, INCOME_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, INCOME_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, INCOME_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LongTermGoalTests(BaseTestCase):

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BudgetGoalTests(BaseTestCase):

    @staticmethod
    def setup_test_models(client):
        # Long Term Goal
        LongTermGoalTests.setup_test_models(client)
        response = create_test_model(client, LONGTERMGOAL_NAME)
        post_data[BUDGETGOAL_NAME]['long_term_goal'] = response.data['url']

        # Budget
        BudgetTests.setup_test_models(client)
        response = create_test_model(client, BUDGET_NAME)
        post_data[BUDGETGOAL_NAME]['budget'] = response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        """
        LIST
        """
        response = list_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        DETAIL
        """
        response = detail_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        POST
        """
        response = post_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        """
        PUT
        """
        response = put_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        DELETE
        """
        response = detail_test(self.client, LONGTERMGOAL_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
