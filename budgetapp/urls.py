from django.conf.urls import url

from . import views

app_name = 'budgetapp'

urlpatterns = [
	url(r'^$', views.test_view, name='test'),
]