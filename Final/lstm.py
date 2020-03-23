import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from datetime import datetime, timedelta 

def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    return numerator / (denominator + 1e-7)
#     return numerator / (denominator)


def ActualScaler(data):
    return data * (test_set_max - test_set_min) + test_set_min



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


# train parameters
seq_length = 50       # sequence length
input_dim = 1          # dimension of input value
output_dim = 1         # dimenstion of output value
learning_rate = 0.01
iterations = 20


# URL for historical rates
URL_HISTORY = 'https://api.exchangeratesapi.io/history'

# Version 1, set dataset for the amount of 3 years
start_at = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
end_at = datetime.today().strftime("%Y-%m-%d")



URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

response = requests.get(URL)
json = response.json()
json = json['rates'].items()

rates = {}
for key, value in sorted(json):
#     print(str(key) + '=>' + str(value))
    rates[key] = value['KRW']
    

df = pd.DataFrame(list(rates.items()), columns=['Date', 'Rate'])

print('Start: ', start_at, '/  End: ', end_at)

period = df.loc[len(df)*0.9 - 1:, 'Date']

df = np.array(df.loc[:, ['Rate']].values)

train_size = int(len(df) * 0.9)
print('Train Size: ', train_size)

train_set = df[0:train_size]
test_set = df[train_size-seq_length:]

print('Train Set Size: ', train_set.shape, 'Test Set Size: ', test_set.shape)

train_set_max = np.max(train_set)
train_set_min = np.min(train_set)
test_set_max = np.max(test_set)
test_set_min = np.min(test_set)

train_set = MinMaxScaler(train_set)
test_set = MinMaxScaler(test_set)

# Dividing training dataset and testing dataset
X_train, y_train = build_window(train_set, seq_length)
X_test, y_test = build_window(test_set, seq_length)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# Step 3. Modelling

# Building model (layer by layer)
tf.model = tf.keras.Sequential()

# Selecting LSTM model
tf.model.add(tf.keras.layers.LSTM(units=1, input_shape=(seq_length, input_dim)))

# tf.model.add(tf.keras.layers.Dropout(0.2))

# Dense layer is just a regular layer of neurons in a neural network.
tf.model.add(tf.keras.layers.Dense(units=output_dim, activation='tanh'))

# Summary of model
tf.model.summary()

# Tuning model
tf.model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])

# Step 4. Training

# Training model
tf.model.fit(X_train, y_train, epochs=iterations)

score = tf.model.evaluate(X_train, y_train, verbose=0)
print(' Train accuracy:', score[1])

tf.model.save('./model/lstm.h5')

# Step 5. Testing

# Testing model
y_predict = tf.model.predict(X_test)

y_predict = ActualScaler(y_predict)
y_test = ActualScaler(y_test)

result = {}
for i in range(0, len(y_predict)):
    result[period.iloc[i]] = y_predict.item(i)

df_result = pd.DataFrame(list(result.items()), columns=['Date', 'Rate'])

# Visualization model
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

# save
