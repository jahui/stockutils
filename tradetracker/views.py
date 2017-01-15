from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Trade
from datetime import date
from decimal import Decimal
import pandas_datareader.data as web

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

@login_required(login_url='/trades/logout')
def logoutTrades(request):
	logout(request)
	return HttpResponseRedirect(reverse('tradetracker:viewTrades'))

@login_required(login_url='/trades/login')
def viewTrades(request):
	current_user = request.user
	trade_list = current_user.trade_set.all()
	portfolio_list = current_user.portfoliostock_set.all()
	prices = {}
	#trade_list = Trade.objects.all()
	total_earnings = 0
	for trade in trade_list:
		total_earnings += trade.price * -trade.shares
		if not trade.ticker in prices:
			prices[trade.ticker] = web.get_quote_yahoo(trade.ticker)["last"].get(trade.ticker)
	context = {'trade_list' : trade_list, 'total_earnings' : total_earnings, 
		'current_user' : request.user.username, 'portfolio_list' : portfolio_list, 'prices' : prices}
	return render(request, 'tradetracker/viewTrades.html', context)


@login_required(login_url='/trades/login')
def addTrades(request):
	return render(request, 'tradetracker/addTrades.html', 
		{'current_user' : request.user.username})

@login_required(login_url='/trades/login')
def saveTrade(request):
	current_user = request.user
	ticker = request.POST['ticker'].upper()
	trade_date = request.POST['tradedate']
	price = Decimal(request.POST['price'])
	shares = int(request.POST['shares'])
	if ticker and trade_date and price and shares:
		try:
			stock = current_user.portfoliostock_set.get(ticker=ticker)
			if shares > 0:
				new_cost = stock.shares * stock.average_cost
				new_cost += price * shares
				new_cost /= (shares + stock.shares)
				stock.shares += shares
				stock.average_cost = new_cost
				stock.save()
			else:
				shares_left = stock.shares + shares
				if shares_left > 0:
					stock.shares = shares_left
					stock.save()
				elif shares_left == 0:
					stock.delete()
				else:
					return render(request, 'tradetracker/addTrades.html', 
						{'error_message' : "Invalid amount!", 'current_user' : request.user.username})
			# moved trade creation to end in case of error
			trade = current_user.trade_set.create(ticker=ticker, trade_date=trade_date, price=price, shares=shares)
		except ObjectDoesNotExist:
			current_user.portfoliostock_set.create(ticker=ticker, average_cost=price, shares=shares)
			# moved trade creation to end in case of error
			trade = current_user.trade_set.create(ticker=ticker, trade_date=trade_date, price=price, shares=shares)
		return HttpResponseRedirect(reverse('tradetracker:viewTrades'))
	else:
		return render(request, 'tradetracker/addTrades.html', 
			{'error_message' : "All fields must be filled!", 'current_user' : request.user.username})

@login_required(login_url='/trades/login')
def editTrades(request):
	current_user = request.user
	trade_list = current_user.trade_set.all()
	total_earnings = 0
	for trade in trade_list:
		total_earnings += trade.price * -trade.shares
	context = {'trade_list' : trade_list, 'total_earnings' : total_earnings, 
		'current_user' : request.user.username}
	return render(request, 'tradetracker/editTrades.html', context)

@login_required(login_url='/trades/login')
def editSpecificTrade(request):
	current_user = request.user
	selected_trade = current_user.trade_set.get(pk=request.POST['selectedTrade'])

	if selected_trade:
		# date needs to be formatted to properly default
		raw_date = selected_trade.trade_date
		# comes in format: Nov. 19, 2016, needs to be YYYY-MM-DD
		format_date = raw_date.isoformat()
		return render(request, 'tradetracker/editSpecificTrade.html', 
			{'selected_trade' : selected_trade, 'format_date' : format_date, 
				'current_user' : request.user.username})
	else:
		#rebuild the editTrades page with the error message
		current_user = request.user
		trade_list = current_user.trade_set.all()
		total_earnings = 0
		for trade in trade_list:
			total_earnings += trade.price * -trade.shares
		context = {'trade_list' : trade_list, 'total_earnings' : total_earnings, 
			'current_user' : request.user.username, 'error_message' : "Invalid trade selected!"}
		return render(request, 'tradetracker/editTrades.html', context)

@login_required(login_url='/trades/login')
def changeTrade(request):
	current_user = request.user
	selected_trade = current_user.trade_set.get(pk=request.POST['selectedTrade'])
	#selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	ticker = request.POST['ticker'].upper()
	trade_date = request.POST['tradedate']
	price = request.POST['price']
	shares = request.POST['shares']

	if ticker and trade_date and price and shares and selected_trade:
		# save values for rollback
		old_ticker = selected_trade.ticker
		old_price = selected_trade.price
		old_shares = selected_trade.shares
		old_date = selected_trade.trade_date

		selected_trade.ticker = ticker
		selected_trade.price = price
		selected_trade.shares = shares
		selected_trade.trade_date = trade_date
		selected_trade.save()

		# todo: what if the edit changes the ticker?
		trades = current_user.trade_set.filter(ticker=ticker)
		avg_cost = 0
		num_bought = 0
		num_sold = 0
		for t in trades:
			if t.shares > 0:
				avg_cost += t.price * t.shares
				num_bought += t.shares
			else:
				num_sold += t.shares
		net_shares_count = num_bought + num_sold
		if net_shares_count > 0:
			try:
				avg_cost /= num_bought
				portfolio_entry = current_user.portfoliostock_set.get(ticker=ticker)
				portfolio_entry.average_cost = avg_cost
				portfolio_entry.shares = net_shares_count
				portfolio_entry.save()
			except ObjectDoesNotExist:
				current_user.portfoliostock_set.create(ticker=ticker, average_cost=avg_cost, shares=net_shares_count)
		elif net_shares_count == 0:
			try:
				portfolio_entry = current_user.portfoliostock_set.get(ticker=old_ticker)
				portfolio_entry.delete()
			except ObjectDoesNotExist:
				# do nothing
				nothing = 1
		else:
			# rollback the trade save
			selected_trade.ticker = old_ticker
			selected_trade.price = old_price
			selected_trade.shares = old_shares
			selected_trade.trade_date = old_date
			selected_trade.save()
			return render(request, 'tradetracker/editSpecificTrade.html', 
				{'selected_trade': selected_trade, 'error_message' : "Invalid no. of shares!", 
				'current_user' : request.user.username})

		
		return HttpResponseRedirect(reverse('tradetracker:viewTrades'))
	else:
		return render(request, 'tradetracker/editSpecificTrade.html', 
			{'selected_trade': selected_trade, 'error_message' : "All fields must be filled!", 
				'current_user' : request.user.username})

@login_required(login_url='/trades/login')
def deleteTrade(request):
	current_user = request.user
	selected_trade = current_user.trade_set.get(pk=request.POST['selectedTrade'])
	#selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	if selected_trade:
		# old values for rollback
		old_ticker = selected_trade.ticker
		old_price = selected_trade.price
		old_shares = selected_trade.shares
		old_date = selected_trade.trade_date

		selected_trade.delete()

		trades = current_user.trade_set.filter(ticker=old_ticker)
		avg_cost = 0
		num_bought = 0
		num_sold = 0
		for t in trades:
			if t.shares > 0:
				avg_cost += t.price * t.shares
				num_bought += t.shares
			else:
				num_sold += t.shares
		net_shares_count = num_bought + num_sold
		if net_shares_count > 0:
			try:
				avg_cost /= num_bought
				portfolio_entry = current_user.portfoliostock_set.get(ticker=old_ticker)
				portfolio_entry.average_cost = avg_cost
				portfolio_entry.shares = net_shares_count
				portfolio_entry.save()
			except ObjectDoesNotExist:
				current_user.portfoliostock_set.create(ticker=old_ticker, average_cost=avg_cost, shares=net_shares_count)
		elif net_shares_count == 0:
			try:
				portfolio_entry = current_user.portfoliostock_set.get(ticker=old_ticker)
				portfolio_entry.delete()
			except ObjectDoesNotExist:
				# do nothing
				nothing = 1
		else:
			# recreate the old trade
			trade = current_user.trade_set.create(ticker=old_ticker, trade_date=old_date, price=old_price, shares=old_shares)
			return render(request, 'tradetracker/editSpecificTrade.html', 
				{'selected_trade': selected_trade, 'error_message' : "Invalid no. of shares!", 
				'current_user' : request.user.username})
	# todo: error message for this?
	return HttpResponseRedirect(reverse('tradetracker:viewTrades'))
