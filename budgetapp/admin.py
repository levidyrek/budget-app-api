from django.contrib import admin
from .models import (Budget, CategoryBudgetGroup, Category, CategoryBudget,
					 Transaction, Income, LongTermGoal, BudgetGoal)


class BudgetAdmin(admin.ModelAdmin):
	list_display = ('month', 'year', 'owner')


admin.site.register(Budget, BudgetAdmin)
admin.site.register(CategoryBudgetGroup)
admin.site.register(Category)
admin.site.register(CategoryBudget)
admin.site.register(Income)
admin.site.register(LongTermGoal)
admin.site.register(BudgetGoal)
admin.site.register(Transaction)
