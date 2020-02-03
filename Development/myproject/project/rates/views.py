from django.shortcuts import render

from datetime import datetime
import requests

# Create your views here.
url = 'https://api.ratesapi.io/api/latest'

def rates(request):
    # Making our request
    response = requests.get(url)
    data = response.json()
    today = datetime.strptime(data['date'], "%Y-%M-%d").date()
    today = today.strftime("%d / %b / %Y")
    return render(request, 'home.html', {'base': data['base'], 'date': today, 'rates': data['rates']})
    # return render(request, 'home.html', {'rates' :CurrencyRates().get_rates('EUR', date.today())})

