from django.contrib import admin
from .models import (Budget, BudgetCategoryGroup, BudgetCategory,
                     Transaction, Income, LongTermGoal, BudgetGoal)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'owner')


class BudgetCategoryGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget')


class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'group')


class BudgetGoalAdmin(admin.ModelAdmin):
    list_display = ('budget', 'long_term_goal', 'goal_amount',
                    'progress',)


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('budget', 'name', 'amount',)


class LongTermGoalAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'goal_amount', 'progress',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'recipient', 'budget_category', 'date',)


admin.site.register(Budget, BudgetAdmin)
admin.site.register(BudgetCategoryGroup, BudgetCategoryGroupAdmin)
admin.site.register(BudgetCategory, BudgetCategoryAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(LongTermGoal, LongTermGoalAdmin)
admin.site.register(BudgetGoal, BudgetGoalAdmin)
admin.site.register(Transaction, TransactionAdmin)
