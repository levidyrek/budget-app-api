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
USER_NAME = 'user'

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
    USER_NAME: {'username': 'test', 'email': 'test@test.com', 'password': 'test'}
}
test_users = [
    {'username': 'test0', 'email': 'test0@test.com', 'password': 'test0'},
    {'username': 'test1', 'email': 'test1@test.com', 'password': 'test1'},
]


# ------- Helper Functions ------- #


def create_test_users():
    """
    Creates test users from test_users data
    """
    for test_user in test_users:
        User.objects.create_user(username=test_user['username'],
                                 email=test_user['email'],
                                 password=test_user['password'])


def login_test_user(client, index=0):
    """
    Logs in selected test user
    :param client: 
    :param index: The index of the desired user in test_users
    :return: 
    """
    user = User.objects.get(username=test_users[index]['username'])
    if user is None:
        raise Exception('Test user does not exist')
    client.force_login(user)


def create_test_model(client, model_name, test_user_index=0):
    """
    Logs in as test user (create_test_users must be called first) and
    calls the test model function corresponding to the given name
    :param client: 
    :param model_name: Name of the model to be created
    :return: The post response
    """
    login_test_user(client, test_user_index)

    url = app_name + ':' + model_name + '-list'
    test_data = post_data[model_name]

    response = client.post(reverse(url), test_data)
    if response.status_code != status.HTTP_201_CREATED:
        raise Exception('Test ' + model_name + ' could not be created: ' +
                        str(response.data))

    client.logout()

    return response


def list_test(client, model_name, auth=False, test_user_index=0):
    url = app_name + ':' + model_name + '-list'
    if auth:
        login_test_user(client, test_user_index)
    response = client.get(reverse(url))
    if auth:
        client.logout()
    return response


def post_test(client, model_name, auth=False, test_user_index=0):
    url = app_name + ':' + model_name + '-list'
    if auth:
        login_test_user(client, test_user_index)
    response = client.post(reverse(url), post_data[model_name])
    if auth:
        client.logout()
    return response


def detail_test(client, model_name, auth=False, test_user_index=0):
    response = create_test_model(client, model_name)
    if auth:
        login_test_user(client, test_user_index)
    response = client.get(response.data['url'])
    if auth:
        client.logout()
    return response


def put_test(client, model_name, auth=False, test_user_index=0):
    response = create_test_model(client, model_name)
    if auth:
        login_test_user(client, test_user_index)
    response = client.put(response.data['url'], post_data[model_name])
    if auth:
        client.logout()
    return response


def delete_test(client, model_name, auth=False, test_user_index=0):
    response = create_test_model(client, model_name)
    if auth:
        login_test_user(client, test_user_index)
    response = client.delete(response.data['url'])
    if auth:
        client.logout()
    return response


class BaseTestCase(APITestCase):

    def setUp(self):
        create_test_users()
        self.setup_test_models(self.client)

    @staticmethod
    def setup_test_models(client):
        pass


class BudgetTests(BaseTestCase):
    """
    Ensures the actions (POST, PUT, LIST, DETAIL, DELETE) work as expected with
    and without authentication
    """

    model_name = BUDGET_NAME

    # --------- No Authentication tests ---------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------- Cross-User Actions ----------- #

    # def test_detail_cross_user(self):
    #     response = detail_test(self.client, self.model_name, True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_post_cross_user(self):
    #     response = post_test(self.client, self.model_name, True)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_put_cross_user(self):
    #     response = put_test(self.client, self.model_name, True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_delete_cross_user(self):
    #     response = detail_test(self.client, self.model_name, True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryTests(BaseTestCase):

    model_name = CATEGORY_NAME

    # --------- No authentication tests --------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryBudgetGroupTests(BaseTestCase):

    model_name = CATEGORYBUDGETGROUP_NAME

    @staticmethod
    def setup_test_models(client):
        # Test budget
        BudgetTests.setup_test_models(client)
        response = create_test_model(client, BUDGET_NAME)
        post_data[CATEGORYBUDGETGROUP_NAME]['budget'] = response.data['url']

    # --------- No authentication tests --------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryBudgetTests(BaseTestCase):

    model_name = CATEGORYBUDGET_NAME

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
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TransactionTests(BaseTestCase):

    model_name = TRANSACTION_NAME

    @staticmethod
    def setup_test_models(client):
        # Category Budget
        CategoryBudgetTests.setup_test_models(client)
        response = create_test_model(client, CATEGORYBUDGET_NAME)
        post_data[TRANSACTION_NAME]['category_budget'] = response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IncomeTests(BaseTestCase):

    model_name = INCOME_NAME

    @staticmethod
    def setup_test_models(client):
        # Budget
        BudgetTests.setup_test_models(client)
        response = create_test_model(client, BUDGET_NAME)
        post_data[INCOME_NAME]['budget'] = response.data['url']

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LongTermGoalTests(BaseTestCase):

    model_name = LONGTERMGOAL_NAME

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BudgetGoalTests(BaseTestCase):

    model_name = BUDGETGOAL_NAME

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
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        response = post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_auth(self):
        response = put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        response = detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------- Authentication Tests ------------ #

    def test_list_auth(self):
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        response = post_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        response = put_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        response = detail_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(BaseTestCase):

    model_name = USER_NAME
    detail_url = None

    def setUp(self):
        super(UserTests, self).setUp()
        test_pk = User.objects.get(username=test_users[0]['username']).pk
        self.detail_url = reverse(app_name + ':' + self.model_name + '-detail',
                                  args=[test_pk])

    # -------- No authentication tests -------- #

    def test_list_no_auth(self):
        response = list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_no_auth(self):
        """
        Note: Should succeed without authentication 
        """
        url = app_name + ':' + self.model_name + '-create'
        response = self.client.post(reverse(url), post_data[self.model_name])
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
        response = list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_auth(self):
        login_test_user(self.client)
        response = self.client.get(self.detail_url)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_auth(self):
        login_test_user(self.client)
        url = app_name + ':' + self.model_name + '-create'
        response = self.client.post(reverse(url), post_data[self.model_name])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_auth(self):
        login_test_user(self.client)
        response = self.client.put(self.detail_url, post_data[USER_NAME])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_auth(self):
        login_test_user(self.client)
        response = self.client.delete(self.detail_url)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
