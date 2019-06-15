import json
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from ..models import (Budget, BudgetCategory, BudgetCategoryGroup, Payee,
                      Transaction)
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
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], self.group.name)
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '0')

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
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], 'Not Existing')
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '0')

        category = BudgetCategory.objects.get(category='Category 2')
        self.assertEqual(category.group.budget.year, 9999)
        self.assertEqual(category.group.budget.month, 'JAN')
        self.assertEqual(category.category, 'Category 2')
        self.assertEqual(category.group.name, 'Not Existing')
        self.assertEqual(category.limit, 100)
        self.assertEqual(category.spent, Decimal(0))

    def test_budget_category_create_insufficient_fields(self):
        response = self.client.post('/budgetcategories/', {
            'budget_month': 'JAN',
            'category': 'Category 2',
            'group': 'Not Existing',
            'limit': 100,
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
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], self.group.name)
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '0')

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
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['category'], 'Category 2')
        self.assertEqual(data['group'], 'Not Existing')
        self.assertEqual(data['limit'], '100.00')
        self.assertEqual(data['spent'], '0')

        category = BudgetCategory.objects.get(category='Category 2')
        self.assertEqual(category.group.budget.year, 9999)
        self.assertEqual(category.group.budget.month, 'JAN')
        self.assertEqual(category.category, 'Category 2')
        self.assertEqual(category.group.name, 'Not Existing')
        self.assertEqual(category.limit, 100)
        self.assertEqual(category.spent, 0)

    def test_budget_category_update_insufficient_fields(self):
        response = self.client.post('/budgetcategories/', {
            'budget_month': 'JAN',
            'category': 'Category 2',
            'group': 'Not Existing',
            'limit': 100,
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
            }
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['limit'], '200.00')


class TransactionViewTests(TestCase):

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
        )
        self.payee1 = Payee.objects.create(
            name='Payee 1',
            owner=self.user,
        )
        self.payee2 = Payee.objects.create(
            name='Payee 2',
            owner=self.user,
        )
        self.transaction = Transaction.objects.create(
            amount=100,
            payee=self.payee1,
            budget_category=self.category,
            date=date(2019, 1, 16),
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_budget_category_create_payee_existing(self):
        response = self.client.post('/transactions/', {
            'amount': 100,
            'budget_category': self.category.pk,
            'date': '2019-01-16',
            'payee': 'Payee 1'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '100.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Payee 1')

    def test_budget_category_create_payee_not_existing(self):
        response = self.client.post('/transactions/', {
            'amount': 100,
            'budget_category': self.category.pk,
            'date': '2019-01-16',
            'payee': 'Non-Existing Payee'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '100.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Non-Existing Payee')

    def test_budget_category_put_payee_existing(self):
        response = self.client.put(
            '/transactions/{}/'.format(self.transaction.pk), {
                'amount': 100,
                'budget_category': self.category.pk,
                'date': '2019-01-16',

                'payee': 'Payee 2'
            })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '100.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Payee 2')

    def test_budget_category_put_payee_not_existing(self):
        response = self.client.put(
            '/transactions/{}/'.format(self.transaction.pk), {
                'amount': 100,
                'budget_category': self.category.pk,
                'date': '2019-01-16',

                'payee': 'Non-Existing Payee'
            })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '100.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Non-Existing Payee')

    def test_budget_category_patch_payee_existing(self):
        response = self.client.patch(
            '/transactions/{}/'.format(self.transaction.pk), {
                'payee': 'Payee 2'
            })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '100.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Payee 2')

    def test_budget_category_patch_payee_not_existing(self):
        response = self.client.patch(
            '/transactions/{}/'.format(self.transaction.pk), {
                'payee': 'Non-Existing Payee'
            })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '100.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Non-Existing Payee')

    def test_budget_category_patch_non_payee(self):
        response = self.client.patch(
            '/transactions/{}/'.format(self.transaction.pk), {
                'amount': 200
            })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['amount'], '200.00')
        self.assertEqual(data['budget_category'], self.category.pk)
        self.assertEqual(data['date'], '2019-01-16')
        self.assertEqual(data['payee'], 'Payee 1')


class CopyBudgetViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
        )
        self.budget1 = Budget.objects.create(
            month='JAN',
            year=2000,
            owner=self.user,
        )
        self.group1 = BudgetCategoryGroup.objects.create(
            name='Group 1',
            budget=self.budget1,
        )
        self.category1 = BudgetCategory.objects.create(
            category='Category 1',
            group=self.group1,
            limit=100,
        )
        self.category2 = BudgetCategory.objects.create(
            category='Category 2',
            group=self.group1,
            limit=100,
        )

        self.budget2 = Budget.objects.create(
            month='FEB',
            year=2000,
            owner=self.user,
        )
        self.group2 = BudgetCategoryGroup.objects.create(
            name='Group 2',
            budget=self.budget2,
        )
        self.category3 = BudgetCategory.objects.create(
            category='Category 3',
            group=self.group2,
            limit=200,
        )
        self.category4 = BudgetCategory.objects.create(
            category='Category 4',
            group=self.group2,
            limit=200,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_basic_request(self):
        response = self.client.post('/copy-budget/', {
            'source': self.budget1.pk,
            'target_year': 2000,
            'target_month': 'FEB',
        })
        self.assertEqual(response.status_code, 200)

    def test_bad_request(self):
        response = self.client.post('/copy-budget/', {
            'source': self.budget1.pk,
            'target_year': 2000,
        })
        self.assertEqual(response.status_code, 400)

    def test_copy_existing_to_existing(self):
        response = self.client.post('/copy-budget/', {
            'source': self.budget1.pk,
            'target_year': 2000,
            'target_month': 'FEB',
        })
        self.assertEqual(response.status_code, 200)

        groups = \
            self.budget2.budget_category_groups.values_list('name', flat=True)
        self.assertEqual(list(groups), ['Group 1'])

        categories = (
            self.budget2
            .budget_category_groups.first()
            .budget_categories.values_list('category', flat=True)
        )
        self.assertEqual(list(categories), ['Category 1', 'Category 2'])

    def test_copy_existing_to_nonexisting(self):
        response = self.client.post('/copy-budget/', {
            'source': self.budget1.pk,
            'target_year': 3000,
            'target_month': 'FEB',
        })
        self.assertEqual(response.status_code, 200)

        budget = Budget.objects.get(
            year=3000,
            month='FEB',
            owner=self.user,
        )

        groups = \
            budget.budget_category_groups.values_list('name', flat=True)
        self.assertEqual(list(groups), ['Group 1'])

        categories = (
            budget
            .budget_category_groups.first()
            .budget_categories.values_list('category', flat=True)
        )
        self.assertEqual(list(categories), ['Category 1', 'Category 2'])

    def test_copy_nonexisting(self):
        response = self.client.post('/copy-budget/', {
            'source': -1,
            'target_year': 3000,
            'target_month': 'FEB',
        })
        self.assertEqual(response.status_code, 400)

    def test_copy_another_users(self):
        user = User.objects.create(
            username='test2',
            password='test2',
        )
        budget = Budget.objects.create(
            month='JAN',
            year=2000,
            owner=user,
        )
        response = self.client.post('/copy-budget/', {
            'source': budget.pk,
            'target_year': 3000,
            'target_month': 'FEB',
        })
        self.assertEqual(response.status_code, 400)

    def test_copy_previous_month(self):
        """
        Defaults to the previous month's budget from the target
        month if no source is given.
        """
        response = self.client.post('/copy-budget/', {
            'target_year': 2000,
            'target_month': 'FEB',
        })
        self.assertEqual(response.status_code, 200)

        groups = \
            self.budget2.budget_category_groups.values_list('name', flat=True)
        self.assertEqual(list(groups), ['Group 1'])

        categories = (
            self.budget2
            .budget_category_groups.first()
            .budget_categories.values_list('category', flat=True)
        )
        self.assertEqual(list(categories), ['Category 1', 'Category 2'])

    def test_copy_no_previous_month(self):
        """
        If there is no previous month, all categories are cleared.
        """
        response = self.client.post('/copy-budget/', {
            'target_year': 2000,
            'target_month': 'JAN',
        })
        self.assertEqual(response.status_code, 200)

        groups = \
            self.budget1.budget_category_groups.count()
        self.assertEqual(groups, 0)
