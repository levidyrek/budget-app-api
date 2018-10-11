from django.contrib import admin
from django.urls import include, path

urlpatterns = [
  path(r'admin/', admin.site.urls),
  path(r'api-auth/', include('rest_framework.urls')),
  path(r'', include('budgetapp.urls', namespace='budgetapp')),
]
