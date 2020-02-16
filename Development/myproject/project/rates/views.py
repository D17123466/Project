from django.shortcuts import render

# Rates function
import requests
from datetime import datetime

# Form class
from .forms import Form


# Create your views here.

url_default = 'https://api.exchangerate-api.com/v4/latest/'

## Currency exchange rates
def rates(request):
    # Alpha API
    # base_url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency="
    # units = ["KRW", "USD", "GBP", "GBN", "CZK", "DKK", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", "TRY"]
    # api_key = "&apikey=TOPT2TECD5MVTH6P"
    # data = {}
    # for unit in units:
    #     url = base_url + unit + api_key
    #     response = requests.get(url)
    #     data[unit] = response.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    
    # Exchange Rate API
    # url = 'https://api.exchangerate-api.com/v4/latest/EUR'
    # url = 'https://api.exchangeratesapi.io/latest'
    # url = 'https://data.fixer.io/api/symbols?access_key=24f9cd72bed5b420346a2a16f766efc8'
    url = url_default + "EUR"
    response = requests.get(url)
    json = response.json()

    unit_base = json['base']
    date_updated = datetime.strptime(json['date'], "%Y-%m-%d").date().strftime("%d / %b / %Y")
    
    rates = json['rates'].items()

    return render(request, 'rates.html', {'unit_base' : unit_base, 'date_updated' : date_updated, 'rates' : rates})



def create(request):
    submit = request.GET.get("submit")
    form = Form(request.GET or None)

    if form.is_valid():
        amount_ = form.cleaned_data.get("amount_")
        from_ = form.cleaned_data.get("from_")
        to_ = form.cleaned_data.get("to_")
        url = url_default + from_
        response = requests.get(url)
        json = response.json()
        result = json['rates'][to_] * amount_
        # amount_ = request.GET['amount_']
        # from_ = request.GET['from_']
        # to_ = request.GET['to_']
        
        # context = {'amount': amount_, 'from': from_, 'to': to_}
        # return render(request, 'create.html', {'form': form, 'amount': amount_, 'from': from_, 'to': to_})
        return render(request, 'create.html', {'form': form, 'amount': amount_, 'from': from_, 'result': result, 'to': to_})

    # if (request.GET):
    #     amount_ = request.GET['amount_']
    #     from_ = request.GET['from_']
    #     to_ = request.GET['to_']

    #     return render(request, 'create.html', {'form': form})
    
    return render(request, 'create.html', {'form': form})