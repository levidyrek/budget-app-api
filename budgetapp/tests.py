import datetime

from django.test import TestCase
from datetime import date
from .models import Budget, CategoryGroup, Category, CategoryBudget, Transaction, Income, Goal, LongTermGoal, BudgetGoal

class ModelMethodTests(TestCase):

	def test_is_past_due_with_past_date(self):
		"""
		Should return true
		"""
		temp_date = date.today() - datetime.timedelta(days=30)
		goal = LongTermGoal(due_date=temp_date)
		self.assertIs(goal.is_past_due(), True)

	def test_is_past_due_with_future_date(self):
		"""
		Should return false
		"""
		temp_date = date.today() + datetime.timedelta(days=30)
		goal = LongTermGoal(due_date=temp_date)
		self.assertIs(goal.is_past_due(), False)

	def test_is_past_due_with_current_date(self):
		"""
		Should return false
		"""
		temp_date = date.today()
		goal = LongTermGoal(due_date=temp_date)
		self.assertIs(goal.is_past_due(), False)
