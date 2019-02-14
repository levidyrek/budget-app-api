from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from ..models import Budget, BudgetCategory, BudgetCategoryGroup
from ..serializers import BudgetCategorySerializer


class SerializerTests(TestCase):

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

        self.request_factory = APIRequestFactory()

    def test_budget_category_unique(self):
        serializer = BudgetCategorySerializer(data={
            'budget_year': self.group.budget.year,
            'budget_month': self.group.budget.month,
            'category': 'Category 2',
            'group': self.group.name,
            'limit': 100,
        })
        self.assertTrue(serializer.is_valid())

    def test_budget_category_not_unique(self):
        serializer = BudgetCategorySerializer(data={
            'budget_year': self.group.budget.year,
            'budget_month': self.group.budget.month,
            'category': 'Category 1',
            'group': self.group.name,
            'limit': 100,
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'non_field_errors': ['Category must be unique within this budget.']
        })
