from flask import Flask, render_template, request
import requests
from form import ConverterForm
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta 

# url_default = 'https://api.exchangerate-api.com/v4/latest/'
url_default = 'https://api.exchangeratesapi.io/latest'
url_history = 'https://api.exchangeratesapi.io/history'


# model = tf.keras.models.load_model('model/model.h5')

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'D17123466'
Bootstrap(app)


# Currency Converter & Rates
@app.route('/', methods=['GET', 'POST'])
def main():

    form = ConverterForm()

    # url = url_default + "EUR"
    url = url_default
    response = requests.get(url)
    json = response.json()

    unit_base = json['base']
    date_updated = datetime.strptime(json['date'], "%Y-%m-%d").date().strftime("%d / %b / %Y")

    rates = json['rates'].items()
    rates = [(key, value) for key, value in rates]
    rates = rates[::-1]
    

    if request.method == 'GET':
        return render_template('basic.html', form=form, unit_base=unit_base, date_updated=date_updated, rates=rates)

    if request.method == 'POST':
        amount = request.form['amount']
        from_ = request.form['from_']
        to_ = request.form['to_']

        if from_ != 'EUR' or to_ !='EUR':
            # url = url_default + from_
            url = url_default + '?base=' + from_

            response = requests.get(url)
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

    url = url_history + '?start_at=' + start_at + '&end_at=' + end_at

    response = requests.get(url)
    json = response.json()
    json = json['rates'].items()
    
    # rates = [(key, value) for key, value in json]
    rates = {}
    for key, value in sorted(json):
        # print(str(key) + '=>' + str(value))
        rates[key] = value[unit]

    if request.method == 'GET':
        return render_template('chart.html', rates=rates, unit=unit)
        
    if request.method == 'POST':
        status = 'After'
        return render_template('chart.html', rates=rates, unit=unit)      
        


