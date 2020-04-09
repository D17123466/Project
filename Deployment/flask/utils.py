import tensorflow as tf
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta 
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from sklearn.preprocessing import MinMaxScaler


URL_LIVE = 'https://fxmarketapi.com/apilive?api_key=vVupG3fXW4TUy-WjXQHw&currency=EURKRW,EURGBP,EURUSD,EURNZD,EURCNY,EURCHF,EURJPY,EURSEK,EURAUD,EURHKD,EURCAD,EUREUR'
API_CALL_SEC = 5

URL_DEFAULT = 'https://api.exchangeratesapi.io/'
URL_LATEST = URL_DEFAULT + 'latest'
URL_HISTORY = URL_DEFAULT + 'history'

CURRENCY_BASE = 'EUR'
CURRENCIES = ['KRW', 'GBP', 'USD', 'NZD', 'CNY', 'CHF', 'JPY', 'SEK', 'AUD', 'HKD', 'CAD']
CURRENCIES_NAME = {'KRW':'South Korean won', 'GBP':'Pound sterling', 'USD':'United States dollar', 'NZD':'New Zealand dollar', 'CNY':'Chinese Yuan', 'CHF':'Swiss franc', 'JPY':'Japanese yen', 'SEK':'Swedish krona', 'AUD':'Australian dollar', 'HKD':'Hong Kong dollar', 'CAD':'Canadian dollar'}

SEQ_LENGTH = 50             # Sequence length          
INPUT_DIM = 1               # Dimension of input value
OUTPUT_DIM = 1              # Dimension of output value
LEARNING_RATE = 0.01        # Learning rate
ITERATIONS = 20             # Epoch
PREDICTION_LENGTH = 128



# MongoDB - Async
def updateMongoDB(collection, URL, START_AT, END_AT):
    ''' 
    Update Database 
    '''
    collection.remove({'$or':[{'Date':{'$lt':START_AT}}, {'Date':{'$gt':END_AT}}]})
    DATE = requests.get(URL).json()['date']
    RATES = requests.get(URL).json()['rates']
    LIST={}
    for cur in CURRENCIES:
        # if cur in ['KRW', 'JPY']:
        #     LIST[cur] = '{:,.2f}'.format(RATES[cur])
        # else:
        #     LIST[cur] = '{:,.4f}'.format(RATES[cur])
        LIST[cur] = RATES[cur]
    collection.insert_one({'Date':DATE, 'Rates':LIST})  


def insertMongoDB(collection, URL):
    ''' 
    Insert Database 
    '''
    JSON = requests.get(URL).json()['rates'].items()
    for date, rates in sorted(JSON):
        LIST={}
        for cur in CURRENCIES:
            # if cur in ['KRW', 'JPY']:
            #     LIST[cur] = '{:,.2f}'.format(rates[cur])
            # else:
            #     LIST[cur] = '{:,.4f}'.format(rates[cur])
            LIST[cur] = rates[cur]
        collection.insert_one({'Date':date, 'Rates': LIST})


def asyncMongoDB(collection):
    ''' 
    Async Database 
    '''
    START_AT, LATEST = setPeriod(collection, 10, 'update')
    IsEmpty= True if collection.count_documents({}) == 0 else False
    IsInvalid = True if (collection.count_documents({'Date':{'$lt':START_AT}}) != 0 or collection.count_documents({'Date':{'$eq':LATEST}}) == 0) else False
    if IsEmpty:
        print('MongoDB: INSERT ')
        insertMongoDB(collection, URL_HISTORY + '?start_at=' + START_AT + '&end_at=' + LATEST)
    elif IsInvalid:
        print('MongoDB: UPDATE')
        updateMongoDB(collection, URL_LATEST, START_AT, LATEST)
    else:
        print('MongoDB: UP-TO-DATE')



def getLiveCurrency(socketio, thread_stop):
    '''
    Configuration of currency rate in real time
    '''
    while not thread_stop.is_set():
        JSON = requests.get(URL_LIVE).json()["price"].items()
        LIST={}
        for key, value in JSON:
            '''
            Extraction of only 'to' currency code against 'EUR' currency code
            '''
            LIST[key[3:]] = value
        socketio.emit('live', {'currency': LIST}, namespace='/live')
        socketio.sleep(API_CALL_SEC)  


def getConversion(from_, to_, amount):
    ''' 
    Computation of Conversion 
    '''
    if from_ != to_:
        URL_BASE = URL_DEFAULT + 'latest' + '?base=' + from_
        JSON = requests.get(URL_BASE).json()
        RESULT = f"{float(JSON['rates'][to_]*float(amount)):,}"
    else:
        RESULT = f"{float(amount):,}"
    return RESULT


def getSelectFieldForm():
    ''' 
    Extraction of SelectField'Choices
    '''
    JSON = requests.get(URL_LATEST).json()
    CHOICES = [(key, key) for key in JSON['rates'] if key in CURRENCIES]
    CHOICES.append((CURRENCY_BASE, CURRENCY_BASE))
    CHOICES = CHOICES[::-1]
    return CHOICES


def setPeriod(collection, YEAR, FLAG):
    """
    Configuration of start point and end point from MongoDB for period
    """
    START_AT = (datetime.today() - timedelta(days=365*YEAR)).strftime("%Y-%m-%d")
    if (FLAG=='update'):
        LATEST = requests.get(URL_LATEST).json()['date']
        return START_AT, LATEST
    else:
        END_AT = collection.find({}, {'_id':0, 'Date':1}).sort([('_id', -1)]).limit(1).next()['Date']
        return START_AT, END_AT


def getConvertToArray(DATASET):
    """
    Conversion of data type from DataFrame to Array
    """
    return np.array(DATASET.loc[:, ['Rate']].values)


def buildSlidingWindow(TIME_SERIES, SEQ_LENGTH):
    '''
    Build Sliding Windows
        - 50 Timesteps
        - Each X is a predicted value learned based on each window that has 50 Timesteps
        - The integration of all X's is a prediction dataset
        - e.g. Simple figure

         =============X
          =============X
           =============X
        
                   .
                       .
                           .
                               .
        
                           =============X
                            =============X
                             =============X

    '''
    X = []
    y = []
    for i in range(0, len(TIME_SERIES) - SEQ_LENGTH):
        X.append(TIME_SERIES[i:i + SEQ_LENGTH,:])
        y.append(TIME_SERIES[i + SEQ_LENGTH, [-1]])
    return np.array(X), np.array(y)


def getHistorical(collection, CURRENCY_SELECTED, YEAR):
    ''' 
    Extraction of the historical dataset from N year(s) ago 
    '''
    START_AT, END_AT = setPeriod(collection, YEAR, 'select')
    LIST = {}
    for doc in collection.find({'$and':[{'Date':{'$gte':START_AT}}, {'Date':{'$lte':END_AT}}]}, {'_id':0, 'Date':1, 'Rates.'+CURRENCY_SELECTED:1}):
        d = datetime.strptime(doc['Date'], '%Y-%m-%d').date()
        d = d.strftime('%d/%m/%Y')
        LIST[d] = doc['Rates'][CURRENCY_SELECTED]
    return LIST


def getPrediction(collection, LIST, CURRENCY_SELECTED):
    '''
    Extraction of the predictive dataset
    '''
    INPUT = dict(list(LIST.items())[len(LIST) - PREDICTION_LENGTH - SEQ_LENGTH:])
    INPUT = pd.DataFrame(list(INPUT.items()), columns=['Date', 'Rate'])
    INPUT_ARRAY = getConvertToArray(INPUT)
    scaler = MinMaxScaler(feature_range=(0, 1))
    INPUT_SCALED = scaler.fit_transform(INPUT_ARRAY)
    INPUT_X, _ = buildSlidingWindow(INPUT_SCALED, SEQ_LENGTH)
    LSTM = tf.keras.models.load_model('./models/model_' + CURRENCY_SELECTED  + '.h5')
    PREDICTION_START_AT = (datetime.strptime(setPeriod(collection, 1, "select")[1], '%Y-%m-%d') + timedelta(days=1)).date()
    PREDICTION_END_AT = (datetime.today() + timedelta(days=180)).date()
    DAYS = (PREDICTION_END_AT - PREDICTION_START_AT).days + 1
    DATE = [PREDICTION_START_AT + timedelta(days=d) for d in range(DAYS)]
    DATE_WORKING = []
    for d in DATE:
        if not d.isoweekday() in [6, 7]:
            DATE_WORKING.append(d.strftime('%Y-%m-%d'))
        if len(DATE_WORKING) == PREDICTION_LENGTH:
            break
    PREDICTION = LSTM.predict(INPUT_X)
    PREDICTION_ACTUAL = scaler.inverse_transform(PREDICTION)
    RESULT = {}
    for i in range(0, len(PREDICTION_ACTUAL)):
        d = datetime.strptime(DATE_WORKING[i], '%Y-%m-%d').date()
        d = d.strftime('%d/%m/%Y')
        RESULT[d] = float(PREDICTION_ACTUAL.item(i))
    return RESULT


def getHighestLowest(LIST):
    '''
    Extraction of Highest & Lowest currency rate in N year(s) ago
    '''
    MAXMIN = {}
    MAXMIN[max(LIST, key=LIST.get)] = max(LIST.values())
    MAXMIN[min(LIST, key=LIST.get)] = min(LIST.values())
    return MAXMIN


def setJobScheduler(collection):
    '''
    Configuration of a job running every 1:00 am in background
    '''
    print('Job Scheduler - Configured')
    scheduler = BackgroundScheduler()
    scheduler.add_job(execLearning, 'cron', hour='1', minute='00', id='flask_scheduler_id', args=(collection,))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


def execLearning(collection):
    ''' 
    Learning LSTM models for most traded currencies by value
    This func will be only executed at a specific time by trigger of Job Scheduler
    '''
    for cur in CURRENCIES:
        print('=============================================')
        print('Learning - Start ', cur, ' Model')
        print('=============================================')
        LIST = getHistorical(collection, cur, 5)
        DATASET = pd.DataFrame(list(LIST.items()), columns=['Date', 'Rate'])
        DATASET_ARRAY = getConvertToArray(DATASET)
        TRAIN_SIZE = int(len(DATASET_ARRAY)*0.9)
        TRAIN_SET =DATASET_ARRAY[0:TRAIN_SIZE]
        TEST_SET = DATASET_ARRAY[TRAIN_SIZE-SEQ_LENGTH:]
        scaler = MinMaxScaler(feature_range=(0, 1))
        TRAIN_SET_SCALED = scaler.fit_transform(TRAIN_SET)
        TEST_SET_SCALED = scaler.fit_transform(TEST_SET)
        X_train, y_train = buildSlidingWindow(TRAIN_SET_SCALED, SEQ_LENGTH)
        X_test, y_test = buildSlidingWindow(TEST_SET_SCALED, SEQ_LENGTH)
        tf.model = tf.keras.Sequential()
        tf.model.add(tf.keras.layers.LSTM(units=1, input_shape=(SEQ_LENGTH, INPUT_DIM)))
        tf.model.add(tf.keras.layers.Dense(units=OUTPUT_DIM, activation='tanh'))
        tf.model.summary()
        tf.model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=LEARNING_RATE), metrics=['accuracy'])
        tf.model.fit(X_train, y_train, epochs=ITERATIONS)
        # SCORE = tf.model.evaluate(X_train, y_train, verbose=0)
        # print('Train Accuracy: ', SCORE[1]*100)
        tf.model.save('./models/model_' + cur + '.h5')
        print('=============================================')
        print('Learning - End ', cur, ' Model')
        print('=============================================')
    print('Learning - Completed')



