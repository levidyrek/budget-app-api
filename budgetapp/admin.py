from django.contrib import admin

from .models import Budget, BudgetCategory, BudgetCategoryGroup, Transaction


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'owner')


class BudgetCategoryGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget')


class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'group')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'payee', 'budget_category', 'date',)


admin.site.register(Budget, BudgetAdmin)
admin.site.register(BudgetCategoryGroup, BudgetCategoryGroupAdmin)
admin.site.register(BudgetCategory, BudgetCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
