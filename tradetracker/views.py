from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Trade
from datetime import date

# Create your views here.
def viewTrades(request):
	trade_list = Trade.objects.all()
	total_earnings = 0
	for trade in trade_list:
		total_earnings += trade.price * -trade.shares
	context = {'trade_list' : trade_list, 'total_earnings' : total_earnings}
	return render(request, 'tradetracker/viewTrades.html', context)

def addTrades(request):
	return render(request, 'tradetracker/addTrades.html', {})

def editTrades(request):
	trade_list = Trade.objects.all()
	total_earnings = 0
	for trade in trade_list:
		total_earnings += trade.price * -trade.shares
	context = {'trade_list' : trade_list, 'total_earnings' : total_earnings}
	return render(request, 'tradetracker/editTrades.html', context)

def editSpecificTrade(request):
	selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	# date needs to be formatted to properly default
	raw_date = selected_trade.trade_date
	# comes in format: Nov. 19, 2016, needs to be YYYY-MM-DD
	format_date = raw_date.isoformat()
	return render(request, 'tradetracker/editSpecificTrade.html', 
		{'selected_trade' : selected_trade, 'format_date' : format_date})

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
			{'error_message' : "All fields must be filled!"})

def deleteTrade(request):
	selected_trade = Trade.objects.get(pk=request.POST['selectedTrade'])
	selected_trade.delete()
	return HttpResponseRedirect(reverse('tradetracker:viewTrades'))

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
			{'selected_trade': selected_trade, 'error_message' : "All fields must be filled!"})