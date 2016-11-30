from django.conf.urls import url

from . import views

app_name = 'tradetracker'
urlpatterns = [
	url(r'^login$', views.loginTrades, name='login'),
	url(r'^process_login', views.processLogin, name='processLogin'),
	url(r'^register', views.registerAccount, name='register'),
	url(r'^create_account', views.processCreateAccount, name='processCreateAccount'),
	url(r'^logout', views.logoutTrades, name='logout'),
	url(r'^view_trades/', views.viewTrades, name='viewTrades'),
	url(r'^edit/', views.editTrades, name='editTrades'),
	url(r'^add/', views.addTrades, name='addTrades'),
	url(r'^save/', views.saveTrade, name='saveTrade'),
	url(r'^delete/', views.deleteTrade, name='deleteTrade'),
	url(r'^edit_trade/', views.editSpecificTrade, name='editSpecificTrade'),
	url(r'^change/', views.changeTrade, name='changeTrade'),
]