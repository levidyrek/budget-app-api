from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

app_name = 'budgetapp'

# DRF Router
router = DefaultRouter()
router.register(r'budgets', views.BudgetViewSet)
router.register(r'budgetcategories', views.BudgetCategoryViewSet)
router.register(r'incomes', views.IncomeViewSet)
router.register(r'budgetgoals', views.BudgetGoalViewSet)
router.register(r'longtermgoals', views.LongTermGoalViewSet)
router.register(r'budgetcategorygroups', views.BudgetCategoryGroupViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    url(r'^users/$', views.UserListView.as_view(), name='user-list'),
    url(r'^users/register/$',
        views.UserCreateView.as_view(),
        name='user-create'),
    url(r'^users/get-auth-token/$',
        rest_framework_views.obtain_auth_token,
        'get_auth_token'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserRetrieveUpdateDestroyView.as_view(),
        name='user-detail'),
    url(r'^', include(router.urls)),
]
