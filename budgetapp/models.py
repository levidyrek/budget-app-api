import datetime
import moneyed

from djmoney.models.fields import MoneyField
from django.db import models
from datetime import date


class Budget(models.Model):
	month = models.DateField()

class CategoryGroup(models.Model):
	name = models.CharField(max_length=100)

class Category(models.Model):
	name = models.CharField(max_length=100)
	group = models.ForeignKey(CategoryGroup, on_delete=models.CASCADE)

class CategoryBudget(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
	limit = MoneyField(max_digits=10, decimal_places=2, default=0, default_currency='USD')
	spent = MoneyField(max_digits=10, decimal_places=2, default=0, default_currency='USD')

	def get_money_left(self):
		return self.limit - self.spent

class Transaction(models.Model):
	amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
	recipient = models.CharField(max_length=100)
	category_budget = models.ForeignKey(CategoryBudget, on_delete=models.CASCADE)
	date = models.DateField()

class Income(models.Model):
	name = models.CharField(max_length=100)
	amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
	budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

class Goal(models.Model):
	name = models.CharField(max_length=100)
	goal_amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
	progress = MoneyField(max_digits=10, decimal_places=2, default=0, default_currency='USD')

	def is_met(self):
		return self.progress >= self.goal_amount

	class Meta:
		abstract = True

class LongTermGoal(Goal):
	due_date = models.DateField()

	def is_past_due(self):
		return date.today() > self.due_date

class BudgetGoal(Goal):
	budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
	long_term_goal = models.ForeignKey(LongTermGoal, on_delete=models.CASCADE, null=True)