from django.contrib.auth.models import User
from django.test import TestCase

from budgetapp import models


class BudgetCategoryTests(TestCase):

    def setUp(self):
        user = User.objects.create(
            username='test',
            password='test',
        )
        budget = models.Budget.objects.create(
            month='JAN',
            year=2000,
            owner=user,
        )
        self.group = models.BudgetCategoryGroup.objects.create(
            name='Group 1',
            budget=budget,
        )

    def test_remaining_zero(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
            spent=100,
        )
        self.assertEqual(category.remaining, 0)

    def test_remaining_positive(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=200,
            spent=100,
        )
        self.assertEqual(category.remaining, 100)

    def test_remaining_negative(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
            spent=200,
        )
        self.assertEqual(category.remaining, -100)
