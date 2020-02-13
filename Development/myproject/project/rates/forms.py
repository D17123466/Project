from django import forms
import requests

class Form(forms.Form):
    # Exchange Rate API
    url = 'https://api.exchangerate-api.com/v4/latest/EUR'
    # url = 'https://api.exchangeratesapi.io/latest'
    # url = 'https://data.fixer.io/api/symbols?access_key=24f9cd72bed5b420346a2a16f766efc8'
    response = requests.get(url)
    json = response.json()
    rates = json['rates']
    units = [(key, key) for key in rates]

    amount_ = forms.IntegerField(label="Amount")
    from_ = forms.ChoiceField(label="From", choices=units, widget=forms.Select)
    to_ = forms.ChoiceField(label="To", choices=units, widget=forms.Select)
