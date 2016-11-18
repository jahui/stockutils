from django.shortcuts import render
#from django.http import HttpResponse
from .models import Trade

# Create your views here.
def viewTrades(request):
	trade_list = Trade.objects.all()
	context = {'trade_list' : trade_list}
	return render(request, 'tradetracker/viewTrades.html', context)

def editTrades(request):
	return HttpResponse("You are at the edit page of the trade tracker.")