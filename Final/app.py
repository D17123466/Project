from flask import Flask, render_template, request
import requests
from form import ConverterForm
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from utils import loadTrainedModel, build_window, getConvertToArray, MinMaxScaler, ActualScaler, getPrediction, setPrediction, setJobScheduler
import pandas as pd
import numpy as np
import tensorflow as tf
import os 


# Ignore tensorflow warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# URLs for latest rates and historical rates
URL_DEFAULT = 'https://api.exchangeratesapi.io/latest'
URL_HISTORY = 'https://api.exchangeratesapi.io/history'

# Configure Flask
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'D17123466'
Bootstrap(app)

# Configure Job Scheduler kicking off the task updating the trained LSTM model
setJobScheduler()

# Currency Converter & Rates
@app.route('/', methods=['GET', 'POST'])
def main():
    # Init form
    form = ConverterForm()

    # Get dataset via URL
    URL = URL_DEFAULT
    response = requests.get(URL)
    json = response.json()

    # Set EUR as base currency
    unit_base = json['base']

    # Set the date when the dataset is updated
    date_updated = datetime.strptime(json['date'], "%Y-%m-%d").date().strftime("%d / %b / %Y")

    # Set dictionary {key:value} as date and currency rate respectively
    # Most traded currencies by value
    json_rate = json['rates'].items()
    rates = [(key, value)  for key, value in json_rate if key in ['USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW']]
    rates = rates[::-1]

    # In case of normal
    if request.method == 'GET':
        return render_template('basic.html', form=form, unit_base=unit_base, date_updated=date_updated, rates=rates)

    # In case of mapping the calculated result to currency converter form
    if request.method == 'POST':
        # Get 3 components by a user
        amount = request.form['amount']
        from_ = request.form['from_']
        to_ = request.form['to_']

        # Compute the result of conversion between two pair
        if from_ != 'EUR' or to_ !='EUR':
            URL = URL_DEFAULT + '?base=' + from_
            response = requests.get(URL)
            json = response.json()
            result = float(json['rates'][to_] * float(amount))
        else:
            result = float(amount)

        return render_template('basic.html', amount=amount, result=result, from_=from_, to_=to_, form=form, unit_base=unit_base, date_updated=date_updated, rates=rates)


# Chart displaying historical currency rates
@app.route('/Chart', methods=['GET', 'POST'])
def chart():
    # Set the selected currency
    unit = request.args['Unit']

    # Set start date and end date
    start_at = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_at = datetime.today().strftime("%Y-%m-%d")

    # Set URL to request historical dataset
    URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

    # Get dataset via URL
    response = requests.get(URL)
    json = response.json()
    json = json['rates'].items()

    # Set dictionary {key:value} as date and currency rate respectively
    rates = {}
    for key, value in sorted(json):
        d = datetime.strptime(key, '%Y-%m-%d').date()
        d = d.strftime('%d/%m/%Y')
        rates[d] = float(value[unit])

    # Get Prediction
    results = setPrediction(rates, 50, unit)

    if request.method == 'GET':
        return render_template('chart.html', rates=rates, unit=unit, results=results)
        
    if request.method == 'POST':
        return render_template('chart.html', rates=rates, unit=unit, results=results)      
        
