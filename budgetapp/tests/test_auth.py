from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from ..urls import app_name


# Model Names
BUDGET_NAME = 'budget'
CATEGORY_NAME = 'category'
CATEGORYBUDGETGROUP_NAME = 'categorybudgetgroup'
CATEGORYBUDGET_NAME = 'categorybudget'

# Test Data
post_data = {
    BUDGET_NAME: {'month': 'JAN', 'year': 2017},
    CATEGORY_NAME: {'name': 'Groceries'},
    CATEGORYBUDGETGROUP_NAME: {'name': 'test', 'budget': ''},
    CATEGORYBUDGET_NAME: {'limit': 100, 'spent': 0, 'group': '', 'category': ''}
}
put_data = {
    BUDGET_NAME: {'month': 'FEB', 'year': 2018},
    CATEGORY_NAME: {'name': 'Dining Out'},
    CATEGORYBUDGETGROUP_NAME: {'name': 'test2'},
    CATEGORYBUDGET_NAME: {'limit': 200, 'spent': 100}
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


class BudgetAuthTests(APITestCase):
    """
    Ensures none of the actions (POST, PUT, LIST, DETAIL, DELETE) are allowed
    without authentication
    """

    def setUp(self):
        create_test_user()

    def test_list(self):
        """
        LIST
        """
        response = list_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail(self):
        """
        DETAIL
        """
        response = detail_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        """
        POST
        """
        response = post_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        """
        PUT
        """
        response = put_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """
        DELETE
        """
        response = detail_test(self.client, BUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NoAuthCategoryTests(APITestCase):

    def setUp(self):
        create_test_user()

    def test_list(self):
        """
        LIST
        """
        response = list_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail(self):
        """
        DETAIL
        """
        response = detail_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        """
        POST
        """
        response = post_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        """
        PUT
        """
        response = put_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """
        DELETE
        """
        response = detail_test(self.client, CATEGORY_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NoAuthCategoryBudgetGroupTests(APITestCase):

    def setUp(self):
        create_test_user()

        # Test budget
        response = create_test_model(self.client, BUDGET_NAME)
        post_data[CATEGORYBUDGETGROUP_NAME]['budget'] = response.data['url']

    def test_list(self):
        """
        LIST
        """
        response = list_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail(self):
        """
        DETAIL
        """
        response = detail_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        """
        POST
        """
        response = post_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        """
        PUT
        """
        response = put_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """
        DELETE
        """
        response = detail_test(self.client, CATEGORYBUDGETGROUP_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NoAuthCategoryBudgetTests(APITestCase):

    def setUp(self):
        create_test_user()

        # Test Category
        response = create_test_model(self.client, CATEGORY_NAME)
        post_data[CATEGORYBUDGET_NAME]['category'] = response.data['url']

        # Test Budget
        response = create_test_model(self.client, BUDGET_NAME)
        post_data[CATEGORYBUDGETGROUP_NAME]['budget'] = response.data['url']

        # Test CategoryBudgetGroup
        response = create_test_model(self.client, CATEGORYBUDGETGROUP_NAME)
        post_data[CATEGORYBUDGET_NAME]['group'] = response.data['url']

    def test_list(self):
        """
        LIST
        """
        response = list_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail(self):
        """
        DETAIL
        """
        response = detail_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        """
        POST
        """
        response = post_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        """
        PUT
        """
        response = put_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        """
        DELETE
        """
        response = detail_test(self.client, CATEGORYBUDGET_NAME)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
