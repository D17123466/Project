from django.shortcuts import render

# Rates
from datetime import datetime
import requests

# Converter
from forex_python.converter import CurrencyRates

# Create your views here.

# Rates API
url = 'https://api.ratesapi.io/api/latest'
# url = 'https://api.exchangeratesapi.io/latest'
# url = 'https://data.fixer.io/api/latest'

def rates(request):
    # Making our request
    response = requests.get(url)
    data = response.json()

    # Base currency (Euro)
    base = data['base']

    # Current date
    date = datetime.strptime(data['date'], "%Y-%M-%d").date()
    date = date.strftime("%d / %b / %Y")

    # All currencies
    rates = data['rates'].items()

    # Converter
    if (request.GET):
        print(request.GET['amount'])
        print(request.GET['from'])
        print(request.GET['to'])

    c = CurrencyRates()
    conversion_rate = c.convert('EUR', 'KRW', 0)

    # Mapping to template (home.html)
    return render(request, 'base.html', {'base': base, 'date': date, 'rates': rates, 'conversion_rate': conversion_rate})
    # return render(request, 'home.html', {'rates' :CurrencyRates().get_rates('EUR', date.today())})


# def converter(request):
#     print(request.GET)
#     c = CurrencyRates()
#     conversion_rate = c.convert('EUR', 'KRW', 30000)
#     return render(request, 'base.html', { 'conversion_rate': conversion_rate})