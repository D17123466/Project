from flask import Flask, render_template, request
import requests
from form import ConverterForm
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from predict import loadTrainedModel, build_window, getConvertToArray, MinMaxScaler, ActualScaler, getPredict

import pandas as pd
import numpy as np

# import keras
import tensorflow as tf

import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# URL_DEFAULT = 'https://api.exchangerate-api.com/v4/latest/'

# URLs for latest rates and historical rates
URL_DEFAULT = 'https://api.exchangeratesapi.io/latest'
URL_HISTORY = 'https://api.exchangeratesapi.io/history'

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'D17123466'
Bootstrap(app)

# Currency Converter & Rates
@app.route('/', methods=['GET', 'POST'])
def main():

    form = ConverterForm()

    # URL = URL_DEFAULT + "EUR"
    URL = URL_DEFAULT
    response = requests.get(URL)
    json = response.json()

    unit_base = json['base']
    date_updated = datetime.strptime(json['date'], "%Y-%m-%d").date().strftime("%d / %b / %Y")

    json_rate = json['rates'].items()
    rates = [(key, value)  for key, value in json_rate if key in ['USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW']]
    rates = rates[::-1]
    

    if request.method == 'GET':
        return render_template('basic.html', form=form, unit_base=unit_base, date_updated=date_updated, rates=rates)

    if request.method == 'POST':
        amount = request.form['amount']
        from_ = request.form['from_']
        to_ = request.form['to_']

        if from_ != 'EUR' or to_ !='EUR':
            # URL = URL_DEFAULT + from_
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
    
    unit = request.args['Unit']
    start_at = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_at = datetime.today().strftime("%Y-%m-%d")

    URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

    response = requests.get(URL)
    json = response.json()
    json = json['rates'].items()


    # rates = [(key, value) for key, value in json]
    rates = {}
    for key, value in sorted(json):
        # print(str(key) + '=>' + str(value[unit]))
        d = datetime.strptime(key, '%Y-%m-%d').date()
        d = d.strftime('%d/%m/%Y')
        rates[d] = float(value[unit])


    size = len(rates)
    input_value = dict(list(rates.items())[size-178:])
    df = pd.DataFrame(list(input_value.items()), columns=['Date', 'Rate'])
    df_rate = getConvertToArray(df)
    rate_max = np.max(df_rate, 0)
    rate_min = np.min(df_rate, 0)
    df_set = MinMaxScaler(df_rate)
    df_x, df_y = build_window(df_set, 50)
    model = loadTrainedModel('model_' + unit)
    results = getPredict(model, df_x, rate_max, rate_min)

    if request.method == 'GET':
        return render_template('chart.html', rates=rates, unit=unit, results=results)
        
    if request.method == 'POST':
        # status = 'After'
        return render_template('chart.html', rates=rates, unit=unit, results=results)      
        
