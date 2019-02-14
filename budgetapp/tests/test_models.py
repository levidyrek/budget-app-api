from datetime import datetime

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
        self.payee = models.Payee.objects.create(
            name='Payee 1',
            owner=user,
        )

    def test_remaining_zero(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=100,
            date=datetime.now(),
        )
        self.assertEqual(category.remaining, 0)

    def test_remaining_positive(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=200,
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=100,
            date=datetime.now(),
        )
        self.assertEqual(category.remaining, 100)

    def test_remaining_negative(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=200,
            date=datetime.now(),
        )
        self.assertEqual(category.remaining, -100)

    def test_spent_no_transactions(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
        )
        self.assertEqual(category.spent, 0)

    def test_spent_positive(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=100,
            date=datetime.now(),
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=100,
            date=datetime.now(),
        )
        self.assertEqual(category.spent, 200)

    def test_spent_negative(self):
        category = models.BudgetCategory.objects.create(
            category='Category 1',
            group=self.group,
            limit=100,
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=100,
            date=datetime.now(),
        )
        models.Transaction.objects.create(
            budget_category=category,
            payee=self.payee,
            amount=-200,
            date=datetime.now(),
        )
        self.assertEqual(category.spent, -100)
