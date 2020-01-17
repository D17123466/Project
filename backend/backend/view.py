from django.shortcuts import render

from forex_python.converter import CurrencyRates
from datetime import date

def home(request):
    return render(request, 'home.html')

def rates_api(request):
    c = CurrencyRates()
    t = date(2020, 1, 17)

    return render(request, 'rates_api.html', {'rates' :c.get_rates('EUR', t)})