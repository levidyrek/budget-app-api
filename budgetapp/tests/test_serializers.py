from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from rest_framework.test import force_authenticate

from ..models import Budget, BudgetCategory, BudgetCategoryGroup
from ..serializers import BudgetCategorySerializer


class SerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
        )
        self.user2 = User.objects.create(
            username='test2',
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

        self.request_factory = RequestFactory()

    def test_budget_category_unique(self):
        request = self.request_factory.post('/budgetcategories/')
        request.user = self.user
        serializer = BudgetCategorySerializer(
            data={
                'budget_year': self.group.budget.year,
                'budget_month': self.group.budget.month,
                'category': 'Category 2',
                'group': self.group.name,
                'limit': 100,
            },
            context={
                'request': request,
            },
        )
        self.assertTrue(serializer.is_valid())

    def test_budget_category_not_unique(self):
        request = self.request_factory.post('/budgetcategories/')
        request.user = self.user
        serializer = BudgetCategorySerializer(
            data={
                'budget_year': self.group.budget.year,
                'budget_month': self.group.budget.month,
                'category': 'Category 1',
                'group': self.group.name,
                'limit': 100,
            },
            context={
                'request': request,
            },
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'non_field_errors': ['Category must be unique within this budget.']
        })

    def test_budget_category_not_unique_cross_user(self):
        request = self.request_factory.post('/budgetcategories/')
        request.user = self.user2
        serializer = BudgetCategorySerializer(
            data={
                'budget_year': self.group.budget.year,
                'budget_month': self.group.budget.month,
                'category': 'Category 1',
                'group': self.group.name,
                'limit': 100,
            },
            context={
                'request': request,
            },
        )
        self.assertTrue(serializer.is_valid())
