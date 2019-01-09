from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'budgetapp'

# DRF Router
router = DefaultRouter()
router.register(r'budgets', views.BudgetViewSet)
router.register(r'budgetcategories', views.BudgetCategoryViewSet)
router.register(r'budgetcategorygroups', views.BudgetCategoryGroupViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/register/',
         views.UserCreateView.as_view(),
         name='user-create'),
    path('users/obtain-auth-token/',
         views.ObtainAuthTokenCookieView.as_view(),
         name='obtain-auth-token'),
    path('users/<int:pk>/',
         views.UserRetrieveUpdateDestroyView.as_view(),
         name='user-detail'),
    path('user-info/', views.UserDetailView.as_view(), name='user-info'),
    path('', include(router.urls)),
]
