from django.shortcuts import render

# Rates
from datetime import datetime
import requests

# Converter
from forex_python.converter import CurrencyRates

import decimal

# Create your views here.

# Rates API
url = 'https://api.ratesapi.io/api/latest'
# url = 'https://api.exchangeratesapi.io/latest'
# url = 'https://data.fixer.io/api/latest'
# url = 'https://api.exchangerate-api.com/v4/latest/EUR'

# url = "https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=TOPT2TECD5MVTH6P"
# main_url = base_url + "&from_currency =" + from_currency + "&to_currency =" + to_currency + "&apikey =" + api_key 

def rates(request):
    # Making our request
    response = requests.get(url)
    data = response.json()

    # Base currency (Euro)
    base = data['base']

    # Current date
    date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    date = date.strftime("%d / %b / %Y")

    # All currencies
    rates = data['rates'].items()

    # Converter
    if (request.GET):
        amount = request.GET['amount']
        from_ = request.GET['from']
        to_ = request.GET['to']

        c = CurrencyRates(force_decimal=True)
        conversion_rate = c.convert(from_, to_, decimal.Decimal(amount))

        return render(request, 'base.html', {'base': base, 'date': date, 'rates': rates, 'conversion_rate': conversion_rate, 'from': from_, 'to': to_, 'amount': amount})

    # c = CurrencyRates()
    # conversion_rate = c.convert('EUR', 'KRW', 0)

    # Mapping to template (home.html)
    return render(request, 'base.html', {'base': base, 'date': date, 'rates': rates})
    # return render(request, 'home.html', {'rates' :CurrencyRates().get_rates('EUR', date.today())})


# def converter(request):
#     print(request.GET)
#     c = CurrencyRates()
#     conversion_rate = c.convert('EUR', 'KRW', 30000)
#     return render(request, 'base.html', { 'conversion_rate': conversion_rate})