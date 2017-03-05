from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'budgetapp'

# DRF Router
router = DefaultRouter()
router.register(r'budgets', views.BudgetViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'categorybudgets', views.CategoryBudgetViewSet)
router.register(r'incomes', views.IncomeViewSet)
router.register(r'budgetgoals', views.BudgetGoalViewSet)
router.register(r'longtermgoals', views.LongTermGoalViewSet)
router.register(r'categorybudgetgroups', views.CategoryBudgetGroupViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
]