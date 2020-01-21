from django.shortcuts import render

from forex_python.converter import CurrencyRates
from datetime import date
from datetime import datetime

import requests
# Where USD is the base currency you want to use
url = 'https://api.ratesapi.io/api/latest'


def home(request):
    # Making our request
    response = requests.get(url)
    data = response.json()
    today = datetime.strptime(data['date'], "%Y-%M-%d").date()
    today = today.strftime("%d / %b / %Y")
    return render(request, 'home.html', {'base': data['base'], 'date': today, 'rates': data['rates']})
    # return render(request, 'home.html', {'rates' :CurrencyRates().get_rates('EUR', date.today())})

