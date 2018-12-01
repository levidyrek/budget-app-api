import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from ..models import Budget, BudgetCategory, BudgetCategoryGroup
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


class BudgetCategoryViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
        )
        budget = Budget.objects.create(
            month='JAN',
            year=2000,
            owner=self.user,
        )
        self.group = BudgetCategoryGroup.objects.create(
            name='Group 1',
            budget=budget,
        )
        self.category = BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
            spent=100,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_budget_category_create(self):
        response = self.client.post('/budgetcategories/', {
            'budget_year': self.group.budget.year,
            'budget_month': self.group.budget.month,
            'category': 'Category 2',
            'group': self.group.name,
            'limit': 100,
            'spent': 100,
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], self.group.name)
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '100.00')

    def test_budget_category_create_related_not_existing(self):
        """
        If a budget month/year or group name is given that does
        not match an existing instance, one is created.
        """
        response = self.client.post('/budgetcategories/', {
            'budget_year': 9999,
            'budget_month': 'JAN',
            'category': 'Category 2',
            'group': 'Not Existing',
            'limit': 100,
            'spent': 100,
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], 'Not Existing')
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '100.00')

        category = BudgetCategory.objects.get(category='Category 2')
        self.assertEqual(category.group.budget.year, 9999)
        self.assertEqual(category.group.budget.month, 'JAN')
        self.assertEqual(category.category, 'Category 2')
        self.assertEqual(category.group.name, 'Not Existing')
        self.assertEqual(category.limit, 100)
        self.assertEqual(category.spent, 100)

    def test_budget_category_create_insufficient_fields(self):
        response = self.client.post('/budgetcategories/', {
            'budget_month': 'JAN',
            'category': 'Category 2',
            'group': 'Not Existing',
            'limit': 100,
            'spent': 100,
        })
        self.assertEqual(response.status_code, 400)

    def test_budget_category_update(self):
        response = self.client.put(
            '/budgetcategories/{}/'.format(self.category.id), {
                'budget_year': self.group.budget.year,
                'budget_month': self.group.budget.month,
                'category': 'Category 2',
                'group': self.group.name,
                'limit': 100,
                'spent': 100,
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], self.group.name)
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '100.00')

    def test_budget_category_update_related_not_existing(self):
        """
        If a budget month/year or group name is given that does
        not match an existing instance, one is created.
        """
        response = self.client.put(
            '/budgetcategories/{}/'.format(self.category.id), {
                'budget_year': 9999,
                'budget_month': 'JAN',
                'category': 'Category 2',
                'group': 'Not Existing',
                'limit': 100,
                'spent': 100,
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], 'Not Existing')
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '100.00')

        category = BudgetCategory.objects.get(category='Category 2')
        self.assertEqual(category.group.budget.year, 9999)
        self.assertEqual(category.group.budget.month, 'JAN')
        self.assertEqual(category.category, 'Category 2')
        self.assertEqual(category.group.name, 'Not Existing')
        self.assertEqual(category.limit, 100)
        self.assertEqual(category.spent, 100)

    def test_budget_category_update_insufficient_fields(self):
        response = self.client.post('/budgetcategories/', {
            'budget_month': 'JAN',
            'category': 'Category 2',
            'group': 'Not Existing',
            'limit': 100,
            'spent': 100,
        })
        self.assertEqual(response.status_code, 400)

    def test_budget_category_patch_with_same_values(self):
        response = self.client.patch(
            '/budgetcategories/{}/'.format(self.category.id), {
                'budget_year': self.category.group.budget.year,
                'budget_month': self.category.group.budget.month,
                'category': self.category.category,
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_budget_category_patch_related_not_existing(self):
        response = self.client.patch(
            '/budgetcategories/{}/'.format(self.category.id), {
                'budget_year': 9999,
                'budget_month': 'JAN',
                'group': 'Not Existing',
            }
        )
        self.assertEqual(response.status_code, 200)

        category = BudgetCategory.objects.get(category='Category 1')
        self.assertEqual(category.group.budget.year, 9999)
        self.assertEqual(category.group.budget.month, 'JAN')
        self.assertEqual(category.group.name, 'Not Existing')

    def test_budget_category_patch_year_not_existing(self):
        response = self.client.patch(
            '/budgetcategories/{}/'.format(self.category.id), {
                'budget_year': 9999,
            }
        )
        self.assertEqual(response.status_code, 200)

        category = BudgetCategory.objects.get(category='Category 1')
        self.assertEqual(category.group.budget.year, 9999)
        self.assertEqual(category.group.budget.month, 'JAN')

    def test_budget_category_patch_month_not_existing(self):
        response = self.client.patch(
            '/budgetcategories/{}/'.format(self.category.id), {
                'budget_month': 'DEC',
            }
        )
        self.assertEqual(response.status_code, 200)

        category = BudgetCategory.objects.get(category='Category 1')
        self.assertEqual(category.group.budget.year, 2000)
        self.assertEqual(category.group.budget.month, 'DEC')

    def test_budget_category_patch_group_not_existing(self):
        response = self.client.patch(
            '/budgetcategories/{}/'.format(self.category.id), {
                'group': 'Not Existing',
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['group'], 'Not Existing')

    def test_budget_category_patch_non_unique_fields(self):
        response = self.client.patch(
            '/budgetcategories/{}/'.format(self.category.id), {
                'limit': 200,
                'spent': 200,
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['limit'], '200.00')
        self.assertEqual(data['spent'], '200.00')
