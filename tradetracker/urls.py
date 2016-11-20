from django.conf.urls import url

from . import views

app_name = 'tradetracker'
urlpatterns = [
	url(r'^$', views.viewTrades, name='index'),
	url(r'^view/', views.viewTrades, name='viewTrades'),
	url(r'^edit/', views.editTrades, name='editTrades'),
	url(r'^add/', views.addTrades, name='addTrades'),
	url(r'^save/', views.saveTrade, name='saveTrade'),
	url(r'^delete/', views.deleteTrade, name='deleteTrade'),
	url(r'^edit_trade/', views.editSpecificTrade, name='editSpecificTrade'),
	url(r'^change/', views.changeTrade, name='changeTrade'),
]