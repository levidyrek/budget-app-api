import datetime
from datetime import date

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


class GoalTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
        )

    def test_is_met_equal(self):
        goal = models.LongTermGoal.objects.create(
            name='Goal 1',
            goal_amount=1000.00,
            progress=1000.00,
            due_date=datetime.datetime.now(),
            owner=self.user,
        )
        self.assertTrue(goal.is_met)

    def test_is_met_greater(self):
        goal = models.LongTermGoal.objects.create(
            name='Goal 1',
            goal_amount=1000.00,
            progress=2000.00,
            due_date=datetime.datetime.now(),
            owner=self.user,
        )
        self.assertTrue(goal.is_met)

    def test_is_met_not_met(self):
        goal = models.LongTermGoal.objects.create(
            name='Goal 1',
            goal_amount=1000.00,
            progress=0,
            due_date=datetime.datetime.now(),
            owner=self.user,
        )
        self.assertFalse(goal.is_met)


class LongTermGoalTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
        )

    def test_past_due_past_date(self):
        goal = models.LongTermGoal.objects.create(
            name='Goal 1',
            goal_amount=1000.00,
            progress=1000.00,
            due_date=date.today() - datetime.timedelta(days=1),
            owner=self.user,
        )
        self.assertTrue(goal.is_past_due)

    def test_past_due_future_date(self):
        goal = models.LongTermGoal.objects.create(
            name='Goal 1',
            goal_amount=1000.00,
            progress=1000.00,
            due_date=date.today() + datetime.timedelta(days=1),
            owner=self.user,
        )
        self.assertFalse(goal.is_past_due)

    def test_past_due_current_date(self):
        goal = models.LongTermGoal.objects.create(
            name='Goal 1',
            goal_amount=1000.00,
            progress=1000.00,
            due_date=date.today(),
            owner=self.user,
        )
        self.assertFalse(goal.is_past_due)
