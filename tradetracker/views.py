from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trade
from datetime import date

# Create your views here.

def loginTrades(request):
	return render(request, 'tradetracker/loginTradeTracker.html', {})

def processLogin(request):
	username = request.POST['username']
	password = request.POST['userpassword']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('tradetracker:viewTrades'))
	else:
		error_message = "Authentication failed!"
		return render(request, 'tradetracker/loginTradeTracker.html', {'error' : error_message})

def registerAccount(request):
	return render(request, 'tradetracker/registerAccountPage.html', {})

def processCreateAccount(request):
	user = User.objects.create_user(request.POST['username'], 
		request.POST['useremail'], request.POST['userpassword'])
	user.save()
	return HttpResponseRedirect(reverse('tradetracker:viewTrades'))

@login_required(login_url='/trades/login')
def viewTrades(request):
	trade_list = Trade.objects.all()
	total_earnings = 0
	for trade in trade_list:
		total_earnings += trade.price * -trade.shares
	context = {'trade_list' : trade_list, 'total_earnings' : total_earnings, 
		'current_user' : request.user.username}
	return render(request, 'tradetracker/viewTrades.html', context)

@login_required
def addTrades(request):
	return render(request, 'tradetracker/addTrades.html', 
		{'current_user' : request.user.username})

@login_required
def editTrades(request):
	trade_list = Trade.objects.all()
	total_earnings = 0
	for trade in trade_list:
		total_earnings += trade.price * -trade.shares
	context = {'trade_list' : trade_list, 'total_earnings' : total_earnings, 
		'current_user' : request.user.username}
	return render(request, 'tradetracker/editTrades.html', context)

@login_required
def editSpecificTrade(request):
	selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	# date needs to be formatted to properly default
	raw_date = selected_trade.trade_date
	# comes in format: Nov. 19, 2016, needs to be YYYY-MM-DD
	format_date = raw_date.isoformat()
	return render(request, 'tradetracker/editSpecificTrade.html', 
		{'selected_trade' : selected_trade, 'format_date' : format_date, 
			'current_user' : request.user.username})

@login_required
def saveTrade(request):
	ticker = request.POST['ticker']
	trade_date = request.POST['tradedate']
	price = request.POST['price']
	shares = request.POST['shares']
	if ticker and trade_date and price and shares:
		trade = Trade(ticker=ticker, trade_date=trade_date, price=price, shares=shares)
		trade.save()
		return HttpResponseRedirect(reverse('tradetracker:viewTrades'))
	else:
		return render(request, 'tradetracker/addTrades.html', 
			{'error_message' : "All fields must be filled!", 'current_user' : request.user.username})

@login_required
def deleteTrade(request):
	selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	selected_trade.delete()
	return HttpResponseRedirect(reverse('tradetracker:viewTrades'))

@login_required
def changeTrade(request):
	selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	ticker = request.POST['ticker']
	trade_date = request.POST['tradedate']
	price = request.POST['price']
	shares = request.POST['shares']

	if ticker and trade_date and price and shares:
		selected_trade.ticker = ticker
		selected_trade.price = price
		selected_trade.shares = shares
		selected_trade.trade_date = trade_date
		selected_trade.save()
		return HttpResponseRedirect(reverse('tradetracker:viewTrades'))
	else:
		return render(request, 'tradetracker/editSpecificTrade.html', 
			{'selected_trade': selected_trade, 'error_message' : "All fields must be filled!", 
				'current_user' : request.user.username})