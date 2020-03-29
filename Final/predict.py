import tensorflow as tf
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta 
from apscheduler.schedulers.background import BackgroundScheduler

# Obtain dataset from external source
def getHistoricalDataset(url, unit):
    response = requests.get(url)
    json = response.json()
    json = json['rates'].items()
    rates = {}
    for key, value in sorted(json):
        rates[key] = value[unit]
    dataset = pd.DataFrame(list(rates.items()), columns=['Date', 'Rate'])
    return dataset


# Convert only rate data from the dataset to array datatype 
def getConvertToArray(dataset):
    # global date_predict
    # date_predict = dataset.loc[len(dataset)*size-1:, 'Date']
    dataset_rate = np.array(dataset.loc[:, ['Rate']].values)
    return dataset_rate


def getTrainTestSplit(dataset, size, seq_length):
    # global test_set_max, test_set_min
    train_size = int(len(dataset)*size)
    train_set = dataset[0:train_size]
    test_set = dataset[train_size-seq_length:]
    # test_set_max = np.max(test_set, 0)
    # test_set_min = np.min(test_set, 0)
    return train_set, test_set


# Normalization
def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    return numerator / (denominator)
    # return numerator / (denominator + 1e-7)


# build the dataset method
def build_window(time_series, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series) - seq_length):
        _x = time_series[i:i + seq_length,:]
        _y = time_series[i + seq_length, [-1]]
        dataX.append(_x)
        dataY.append(_y)
    return np.array(dataX), np.array(dataY)


def getModel(input_dim, output_dim, seq_length, learning_rate):
    tf.model = tf.keras.Sequential()
    tf.model.add(tf.keras.layers.LSTM(units=1, input_shape=(seq_length, input_dim)))
    tf.model.add(tf.keras.layers.Dense(units=output_dim, activation='tanh'))
    tf.model.summary()
    tf.model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
    return tf.model


def execTrain(model, X_train, y_train, iterations):
    model.fit(X_train, y_train, epochs=iterations)


def evaluateModel(model, X_train, y_train):
    score = model.evaluate(X_train, y_train, verbose=0)
    print('Train Accuracy: ', score[1]*100)


def saveTrainedModel(model, model_name):
    model.save('./model/' + model_name + '.h5')



def loadTrainedModel(model_name):
    model = tf.keras.models.load_model('./model/' + model_name  + '.h5')
    return model



def getPredict(model, predict_input, rate_max, rate_min):
    predict_start = (datetime.today() + timedelta(days=0)).date()
    predict_end = (datetime.today() + timedelta(days=180)).date()
    days = (predict_end-predict_start).days + 1
    dates = [predict_start + timedelta(days=x) for x in range(days)]
    date = []
    for d in dates:
        if not d.isoweekday() in (6, 7):
            date.append(d.strftime('%Y-%m-%d'))
        if len(date) == 128:
            break

    predict = model.predict(predict_input)
    predict_actual = ActualScaler(predict, rate_max, rate_min)

    results = {}
    for i in range(0, len(predict_actual)):
        # results[date[i]] = round(predict_actual.item(i), 2)
        d = datetime.strptime(date[i], '%Y-%m-%d').date()
        d = d.strftime('%d/%m/%Y')
        results[d] = float((predict_actual.item(i)))
    return results



# Revert Normalized data to actual data
def ActualScaler(data, rate_max, rate_min):
    # print('predict.py: ', test_set_max, test_set_min)
    return data * (rate_max - rate_min) + rate_min


# Set job scheduler 
# Run task every at 01:00 am 
def setJobScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(execMainTask, 'cron', hour='1', id='flask-lstm')
    scheduler.start()


# Set main task
def execMainTask():
    # URL for historical rates
    URL_HISTORY = 'https://api.exchangeratesapi.io/history'

    # Set dataset for the amount of 5 years
    start_at = (datetime.today() - timedelta(days=365*5)).strftime("%Y-%m-%d")
    end_at = datetime.today().strftime("%Y-%m-%d")

    # Set URL
    URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

    # Train parameters
    seq_length = 50        # Sequence length
    input_dim = 1          # Dimension of input value
    output_dim = 1         # Dimension of output value
    learning_rate = 0.01   # Learning rate
    iterations = 20        # Epoch
    size = 0.9             # The portion of the dataset to in the train split

    # Most traded currencies by value
    for unit in ['USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW']:

        # Step 1. Historical dataset 
        dataset = getHistoricalDataset(URL, unit)

        # Step 2. Convert datatype to array 
        dataset_rate = getConvertToArray(dataset)

        # Step 3. Split a train dataset and test dataset
        train_set, test_set = getTrainTestSplit(dataset_rate, size, seq_length)

        # Step 4. Normalization
        train_set = MinMaxScaler(train_set)
        test_set = MinMaxScaler(test_set)

        # Step 5. Build a sliding window
        X_train, y_train = build_window(train_set, seq_length)
        X_test, y_test = build_window(test_set, seq_length)

        # Step 6. Configure a LSTM model
        lstm_model = getModel(input_dim, output_dim, seq_length, learning_rate)

        # Step 7. Training
        execTrain(lstm_model, X_train, y_train, iterations)

        # Step 8. Evaluation
        evaluateModel(lstm_model, X_test, y_test)

        # Step 9. Save the trained model
        saveTrainedModel(lstm_model, 'model_' + unit)