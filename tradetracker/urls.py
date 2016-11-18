from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.viewTrades, name='index'),
	url(r'^view/', views.viewTrades, name='viewTrades'),
	url(r'^edit/', views.editTrades, name='editTrades'),
]