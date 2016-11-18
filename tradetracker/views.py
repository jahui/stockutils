from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Trade
from datetime import date

# Create your views here.
def viewTrades(request):
	trade_list = Trade.objects.all()
	context = {'trade_list' : trade_list}
	return render(request, 'tradetracker/viewTrades.html', context)

def addTrades(request):
	return render(request, 'tradetracker/addTrades.html', {})

def editTrades(request):
	return HttpResponse("You are at the edit page of the trade tracker.")

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