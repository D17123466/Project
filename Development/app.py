from flask import Flask, render_template, request
import requests
from form import ConverterForm
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from utils import *
import pandas as pd
import numpy as np
import tensorflow as tf
import os 
from flask_pymongo import PyMongo


# Configure Flask
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'D17123466'
Bootstrap(app)

# Solution for tensorflow warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ExchangeDB'
mongo = PyMongo(app)
collection = mongo.db.currency
asyncMongoDB(collection)

# Currency Converter & Rates
@app.route('/', methods=['GET', 'POST'])
def main():
    # Init form
    form = ConverterForm()

    # Get dataset via URL
    # URL = URL_DEFAULT
    # response = requests.get(URL)
    # json = response.json()

    # Set EUR as base currency
    # unit_base = json['base']
    # unit_base = CURRENCY_BASE

    # Set the date when the dataset is updated
    # global latest
    # latest = json['date']
    # date_updated = datetime.strptime(latest, "%Y-%m-%d").date().strftime("%d / %b / %Y")

    DATE_UPDATED = datetime.strptime(collection.find({}, {'_id':0, 'Date':1}).sort([('_id', -1)]).limit(1).next()['Date'], "%Y-%m-%d").date().strftime("%d / %b / %Y")

    # Set dictionary {key:value} as date and currency rate respectively
    # Most traded currencies by value
    # json_rate = json['rates'].items()
    # rates = [(key, '{:,.2f}'.format(value)) for key, value in json_rate if key in ['USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW']]
    # rates = rates[::-1]
    LIST = [(cur, rates) for cur, rates in collection.find({}, {'_id':0, 'Rates':1}).sort([('_id', -1)]).limit(1).next()['Rates'].items()]

    # In case of normal
    if request.method == 'GET':
        return render_template('basic.html', form=form, CURRENCY_BASE=CURRENCY_BASE, DATE_UPDATED=DATE_UPDATED, LIST=LIST)

    # In case of mapping the calculated result to currency converter form
    if request.method == 'POST':
        # Get 3 components by a user
        AMOUNT = request.form['amount']
        FROM = request.form['from_']
        TO = request.form['to_']
        RESULT = getConversion(FROM, TO, AMOUNT)
        return render_template('basic.html', AMOUNT=AMOUNT, RESULT=RESULT, FROM=FROM, TO=TO, form=form, CURRENCY_BASE=CURRENCY_BASE, DATE_UPDATED=DATE_UPDATED, LIST=LIST)


# Chart displaying historical currency rates
@app.route('/Chart', methods=['GET', 'POST'])
def chart():


    # Set the selected currency
    CURRENCY_SELECTED = request.args['Unit']
    LIST, END_AT = getChart(collection, CURRENCY_SELECTED)

    # Set start date and end date
    # start_at = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    # end_at = END_AT
    # # end_at = datetime.today().strftime("%Y-%m-%d")
    
    # # Set URL to request historical dataset
    # URL = URL_DEFAULT + 'history' + '?start_at=' + start_at + '&end_at=' + end_at

    # # Get dataset via URL
    # response = requests.get(URL)
    # json = response.json()
    # json = json['rates'].items()

    # # Set dictionary {key:value} as date and currency rate respectively
    # rates = {}
    # for key, value in sorted(json):
    #     d = datetime.strptime(key, '%Y-%m-%d').date()
    #     d = d.strftime('%d/%m/%Y')
    #     rates[d] = float(value[unit])

    # print(rates)


    # Get Prediction
    RESULT = setPrediction(LIST, 50, CURRENCY_SELECTED, END_AT)

    if request.method == 'GET':
        return render_template('chart.html', rates=LIST, unit=CURRENCY_SELECTED, results=RESULT)
        
    if request.method == 'POST':
        return render_template('chart.html', rates=LIST, unit=CURRENCY_SELECTED, results=RESULT)
        


if __name__=='__main__':
    # Configure Job Scheduler kicking off the task updating the trained LSTM model
    setJobScheduler()
    app.run(host='0.0.0.0')