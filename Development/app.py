from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from form import ConverterForm
from utils import *
import os 


''' Configure Flask '''
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'D17123466'
Bootstrap(app)


''' Configure SocketIO '''
socketio = SocketIO(app, async_mode=None, logger=True)


''' Ignoring of tensorflow warning messages '''
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


''' Configure MongoDB '''
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ExchangeDB'
mongo = PyMongo(app)
collection = mongo.db.TimeSeries
asyncMongoDB(collection)


@app.route('/', methods=['GET', 'POST'])
def main():
    '''
    Currency Converter & Currency Rate Table
    - Conversion of currency pairs based on the values obtained by a user
    - Currency Rate Table with Currency flag, code, name, rate, and chart
    '''
    form = ConverterForm()
    LIST = [(cur, rates) for cur, rates in collection.find({}, {'_id':0, 'Rates':1}).sort([('_id', -1)]).limit(1).next()['Rates'].items()]
    if request.method == 'GET':
        '''
        Default
        '''
        return render_template('index.html', form=form, CURRENCY_BASE=CURRENCY_BASE, CURRENCIES=CURRENCIES, CURRENCIES_NAME=CURRENCIES_NAME, LIST=LIST)
    if request.method == 'POST':
        '''
        Currency Converter Form
        - Obtain 3 components (amount, from, to) by a user
        '''
        AMOUNT = request.form['amount']
        FROM = request.form['from_']
        TO = request.form['to_']
        RESULT = getConversion(FROM, TO, AMOUNT)
        return render_template('index.html', AMOUNT=AMOUNT, RESULT=RESULT, FROM=FROM, TO=TO, form=form, CURRENCY_BASE=CURRENCY_BASE, CURRENCIES=CURRENCIES, CURRENCIES_NAME=CURRENCIES_NAME, LIST=LIST)


@socketio.on('connect', namespace='/live')
def connect():
    '''
    Flask-SocketIO
    - Connection with client
    - Calling API request in background figuring out currency rate in real time 
    '''
    THREAD_START = Thread()
    THREAD_END = Event()
    print('Socket - Connected')
    if not THREAD_START.is_alive():
        print('Thread - Executed')
        THREAD_START = socketio.start_background_task(getLiveCurrency, socketio, THREAD_END)


@socketio.on('disconnect', namespace='/live')
def disconnect():
    '''
    Flask-SocketIO
    - Disconnection with client 
    '''
    print('Socket - Disconnected')


@app.route('/Chart', methods=['GET', 'POST'])
def chart():
    '''
    Chart
    - Displaying Time-Series currency rate and Time-Series prediction rate
    '''
    DATE_UPDATED = datetime.strptime(collection.find({}, {'_id':0, 'Date':1}).sort([('_id', -1)]).limit(1).next()['Date'], "%Y-%m-%d").date().strftime("%d / %b / %Y")
    CURRENCY_SELECTED = request.args['Unit']
    LIST_1 = getHistorical(collection, CURRENCY_SELECTED, 1)
    LIST_2 = getHistorical(collection, CURRENCY_SELECTED, 2)
    LIST_3 = getHistorical(collection, CURRENCY_SELECTED, 3)
    LIST_4 = getHistorical(collection, CURRENCY_SELECTED, 4)
    LIST_5 = getHistorical(collection, CURRENCY_SELECTED, 5)
    LIST_1_MAXMIN = getHighestLowest(LIST_1)
    LIST_2_MAXMIN = getHighestLowest(LIST_2)
    LIST_3_MAXMIN = getHighestLowest(LIST_3)
    LIST_4_MAXMIN = getHighestLowest(LIST_4)
    LIST_5_MAXMIN = getHighestLowest(LIST_5)
    RESULT = getPrediction(collection, LIST_1, CURRENCY_SELECTED)
    if request.method == 'GET':
        return render_template('chart.html', LIST_1=LIST_1, LIST_2=LIST_2, LIST_3=LIST_3, LIST_4=LIST_4, LIST_5=LIST_5, LIST_1_MAXMIN=LIST_1_MAXMIN, LIST_2_MAXMIN=LIST_2_MAXMIN, LIST_3_MAXMIN=LIST_3_MAXMIN, LIST_4_MAXMIN=LIST_4_MAXMIN, LIST_5_MAXMIN=LIST_5_MAXMIN, DATE_UPDATED=DATE_UPDATED, CURRENCY_SELECTED=CURRENCY_SELECTED, CURRENCIES_NAME=CURRENCIES_NAME, RESULT=RESULT)
    if request.method == 'POST':
        return render_template('chart.html', LIST_1=LIST_1, LIST_2=LIST_2, LIST_3=LIST_3, LIST_4=LIST_4, LIST_5=LIST_5, LIST_1_MAXMIN=LIST_1_MAXMIN, LIST_2_MAXMIN=LIST_2_MAXMIN, LIST_3_MAXMIN=LIST_3_MAXMIN, LIST_4_MAXMIN=LIST_4_MAXMIN, LIST_5_MAXMIN=LIST_5_MAXMIN, DATE_UPDATED=DATE_UPDATED, CURRENCY_SELECTED=CURRENCY_SELECTED, CURRENCIES_NAME=CURRENCIES_NAME, RESULT=RESULT)


if __name__=='__main__':
    '''
    Run
    Set the Job Scheduler kicking off the selected task updating each LSTM model
    Set the Flask and socketio with host '0.0.0.0' and any port
    '''
    setJobScheduler(collection)
    socketio.run(app, host='0.0.0.0')
