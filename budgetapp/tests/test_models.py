from datetime import datetime

from budgetapp import models
from django.contrib.auth.models import User
from django.test import TestCase


class BudgetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
        )

        self.budget1 = models.Budget.objects.create(
            month='JAN',
            year=2000,
            owner=self.user,
        )
        group1 = models.BudgetCategoryGroup.objects.create(
            name='Budget 1 Group 1',
            budget=self.budget1,
        )
        models.BudgetCategory.objects.create(
            category='Budget 1 Category 1',
            group=group1,
            limit=100,
        )
        models.BudgetCategory.objects.create(
            category='Budget 1 Category 2',
            group=group1,
            limit=200,
        )

        self.budget2 = models.Budget.objects.create(
            month='FEB',
            year=2000,
            owner=self.user,
        )
        group2 = models.BudgetCategoryGroup.objects.create(
            name='Budget 2 Group 1',
            budget=self.budget2,
        )
        models.BudgetCategory.objects.create(
            category='Budget 2 Category 1',
            group=group2,
            limit=100,
        )
        models.BudgetCategory.objects.create(
            category='Budget 2 Category 2',
            group=group2,
            limit=200,
        )

    def test_copy(self):
        self.budget1.copy_categories(self.budget2)

        # Groups are copied.
        groups = list(
            self.budget1.budget_category_groups
            .order_by('name')
            .values_list('name', flat=True)
        )
        self.assertEqual(groups, ['Budget 2 Group 1'])

        # Categories are copied.
        categories = list(
            models.BudgetCategory.objects.filter(
                group__budget=self.budget1,
            )
            .order_by('category')
            .values_list('category', flat=True)
        )
        self.assertEqual(categories, [
            'Budget 2 Category 1', 'Budget 2 Category 2',
        ])

    def test_previous(self):
        self.assertEqual(self.budget2.previous, self.budget1)

    def test_previous_none(self):
        self.assertEqual(self.budget1.previous, None)

    def test_previous_jan(self):
        jan_99 = models.Budget.objects.create(
            month='DEC',
            year=1999,
            owner=self.user,
        )
        self.assertEqual(self.budget1.previous, jan_99)


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
