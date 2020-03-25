import tensorflow as tf
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta 


# # URL for historical rates
# URL_HISTORY = 'https://api.exchangeratesapi.io/history'

# # Version 1, set dataset for the amount of 3 years
# start_at = (datetime.today() - timedelta(days=365*5)).strftime("%Y-%m-%d")
# end_at = datetime.today().strftime("%Y-%m-%d")

# URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

# # train parameters
# seq_length = 50       # sequence length
# input_dim = 1          # dimension of input value
# output_dim = 1         # dimenstion of output value
# learning_rate = 0.01
# iterations = 20
# size = 0.9 # the portion of the dataset to in the train split

# Normalization
def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    return numerator / (denominator + 1e-7)
#     return numerator / (denominator)


# Revert Normalized data to actual data
def ActualScaler(data, rate_max, rate_min):
    # print('predict.py: ', test_set_max, test_set_min)
    return data * (rate_max - rate_min) + rate_min


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
# response = requests.get(URL)
# json = response.json()
# json = json['rates'].items()

# rates = {}
# for key, value in sorted(json):
# #     print(str(key) + '=>' + str(value))
#     rates[key] = value['KRW']
    
def getTrainTestSplite(dataset, size, seq_length):
    # global test_set_max, test_set_min
    train_size = int(len(dataset)*size)
    train_set = dataset[0:train_size]
    test_set = dataset[train_size-seq_length:]
    # test_set_max = np.max(test_set, 0)
    # test_set_min = np.min(test_set, 0)
    return train_set, test_set


def getModel(input_dim, output_dim, seq_length, learning_rate):
    tf.model = tf.keras.Sequential()
    tf.model.add(tf.keras.layers.LSTM(units=1, input_shape=(seq_length, input_dim)))
    tf.model.add(tf.keras.layers.Dense(units=output_dim, activation='tanh'))
    tf.model.summary()
    tf.model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
    return tf.model


def executeTrain(model, X_train, y_train, iterations):
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
    predict_end = (datetime.today() + timedelta(days=178)).date()
    days = (predict_end-predict_start).days + 1
    dates = [predict_start + timedelta(days=x) for x in range(days)]
    date = []
    for d in dates:
        if not d.isoweekday() in (6, 7):
            date.append(d.strftime('%Y-%m-%d'))
    
    predict = model.predict(predict_input)
    predict_actual = ActualScaler(predict, rate_max, rate_min)

    results = {}
    for i in range(0, len(predict_actual)):
        # results[date[i]] = round(predict_actual.item(i), 2)
        d = datetime.strptime(date[i], '%Y-%m-%d').date()
        d = d.strftime('%d/%m/%Y')
        results[d] = float(round(predict_actual.item(i), 2))
    return results
    


# dataset = getHistoricalDataset(URL, 'KRW')

# dataset_rate = getConvertToArray(dataset)

# train_set, test_set = getTrainTestSplite(dataset_rate, 0.9)

# train_set = MinMaxScaler(train_set)
# test_set = MinMaxScaler(test_set)

# X_train, y_train = build_window(train_set, seq_length)
# X_test, y_test = build_window(test_set, seq_length)



# lstm_model = getModel()

# executeTrain(lstm_model, X_train, y_train)

# evaluateModel(lstm_model, X_test, y_test)

# saveTrainedModel(lstm_model)


# tf.model.save('./model/lstm.h5')

# # Building model (layer by layer)
# tf.model = tf.keras.Sequential()

# # Selecting LSTM model
# tf.model.add(tf.keras.layers.LSTM(units=1, input_shape=(seq_length, input_dim)))

# # tf.model.add(tf.keras.layers.Dropout(0.2))

# # Dense layer is just a regular layer of neurons in a neural network.
# tf.model.add(tf.keras.layers.Dense(units=output_dim, activation='tanh'))

# # Summary of model
# tf.model.summary()

# # Tuning model
# tf.model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])

# Step 4. Training

# Training model
# tf.model.fit(X_train, y_train, epochs=iterations)

# score = tf.model.evaluate(X_train, y_train, verbose=0)
# print(' Train accuracy:', score[1])


# model = tf.keras.models.load_model('./model/lstm.h5')



# Step 5. Testing

# Testing model
# y_predict = tf.model.predict(X_test)

# y_predict = ActualScaler(y_predict)
# y_test = ActualScaler(y_test)

# result = {}
# for i in range(0, len(y_predict)):
#     result[date_predict.iloc[i]] = y_predict.item(i)

# df_result = pd.DataFrame(list(result.items()), columns=['Date', 'Rate'])



# model = loadTrainedModel()

# y_predict = model.predict(X_test)

# y_predict = ActualScaler(y_predict)
# y_test = ActualScaler(y_test)

# result = {}
# for i in range(0, len(y_predict)):
#     result[date_predict.iloc[i]] = y_predict.item(i)

# df_result = pd.DataFrame(list(result.items()), columns=['Date', 'Rate'])



# # Visualization model
# plt.style.use('seaborn')
# plt.figure(figsize=(20, 10))
# plt.xticks(size=10, rotation='horizontal')
# plt.plot(y_test, marker='o')
# plt.plot(y_predict, marker='o')
# plt.title('Currency Exchange Rates', size=40)
# plt.xlabel("Period")
# plt.ylabel("Rates")
# plt.legend(labels=['Actual Rates', 'Prediction Rates'], loc='best', fontsize=20)
# plt.show()

