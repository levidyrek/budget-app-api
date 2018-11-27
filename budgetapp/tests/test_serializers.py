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
            spent=100,
        )

        self.request_factory = APIRequestFactory()

    def test_budget_category_unique(self):
        serializer = BudgetCategorySerializer(data={
            'budget_year': self.group.budget.year,
            'budget_month': self.group.budget.month,
            'category': 'Category 2',
            'group': self.group.name,
            'limit': 100,
            'spent': 100,
        })
        self.assertTrue(serializer.is_valid())

    def test_budget_category_not_unique(self):
        serializer = BudgetCategorySerializer(data={
            'budget_year': self.group.budget.year,
            'budget_month': self.group.budget.month,
            'category': 'Category 1',
            'group': self.group.name,
            'limit': 100,
            'spent': 100,
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {
            'non_field_errors': ['Category must be unique within this budget.']
        })

    def test_budget_category_create_related_existing(self):
        request = self.request_factory.post('/budgetcategories/')
        request.user = self.user
        serializer = BudgetCategorySerializer(data={
            'budget_year': self.group.budget.year,
            'budget_month': self.group.budget.month,
            'category': 'Category 2',
            'group': self.group.name,
            'limit': 100,
            'spent': 100,
        }, context={
            'request': request,
        })
        self.assertTrue(serializer.is_valid())

        instance = serializer.save()
        self.assertEqual(instance.category, 'Category 2')
        self.assertEqual(instance.group, self.group)
        self.assertEqual(instance.limit, 100)
        self.assertEqual(instance.spent, 100)

    def test_budget_category_create_related_not_existing(self):
        request = self.request_factory.post('/budgetcategories/')
        request.user = self.user
        serializer = BudgetCategorySerializer(data={
            'budget_year': 9999,
            'budget_month': 'JAN',
            'category': 'Category 2',
            'group': 'Not Existing',
            'limit': 100,
            'spent': 100,
        }, context={
            'request': request,
        })
        self.assertTrue(serializer.is_valid())

        instance = serializer.save()
        self.assertEqual(instance.group.budget.year, 9999)
        self.assertEqual(instance.group.budget.month, 'JAN')
        self.assertEqual(instance.category, 'Category 2')
        self.assertEqual(instance.group.name, 'Not Existing')
        self.assertEqual(instance.limit, 100)
        self.assertEqual(instance.spent, 100)

    def test_budget_category_update_related_not_existing(self):
        request = self.request_factory.put(
            '/budgetcategories/{}'.format(self.category.id))
        request.user = self.user
        serializer = BudgetCategorySerializer(
            instance=self.category,
            context={
                'request': request,
            }
        )

        instance = serializer.update(self.category, {
            'budget_year': 9999,
            'budget_month': 'JAN',
            'group': {
                'name': 'Not Existing'
            },
        })
        self.assertEqual(instance.group.budget.year, 9999)
        self.assertEqual(instance.group.budget.month, 'JAN')
        self.assertEqual(instance.category, 'Category 1')
        self.assertEqual(instance.group.name, 'Not Existing')
        self.assertEqual(instance.limit, 100)
        self.assertEqual(instance.spent, 100)
