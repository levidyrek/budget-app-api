from django.contrib import admin
from .models import (Budget, BudgetCategoryGroup, Category, BudgetCategory,
					 Transaction, Income, LongTermGoal, BudgetGoal)


class BudgetAdmin(admin.ModelAdmin):
	list_display = ('month', 'year', 'owner')


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('owner', 'name')


class BudgetCategoryGroupAdmin(admin.ModelAdmin):
	list_display = ('owner', 'name', 'budget')


class BudgetCategoryAdmin(admin.ModelAdmin):
	list_display = ('owner', 'category', 'group')


class BudgetGoalAdmin(admin.ModelAdmin):
	list_display = ('owner', 'budget', 'long_term_goal', 'goal_amount', 'progress',)


class IncomeAdmin(admin.ModelAdmin):
	list_display = ('owner', 'budget', 'name', 'amount',)


class LongTermGoalAdmin(admin.ModelAdmin):
	list_display = ('owner', 'name', 'goal_amount', 'progress',)


class TransactionAdmin(admin.ModelAdmin):
	list_display = ('owner', 'amount', 'recipient', 'budget_category', 'date',)


admin.site.register(Budget, BudgetAdmin)
admin.site.register(BudgetCategoryGroup, BudgetCategoryGroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BudgetCategory, BudgetCategoryAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(LongTermGoal, LongTermGoalAdmin)
admin.site.register(BudgetGoal, BudgetGoalAdmin)
admin.site.register(Transaction, TransactionAdmin)
