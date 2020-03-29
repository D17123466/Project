import tensorflow as tf
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import requests
from datetime import datetime, timedelta 
from predict import getHistoricalDataset, getConvertToArray, getTrainTestSplite, MinMaxScaler, build_window, getModel, executeTrain, evaluateModel, saveTrainedModel, loadTrainedModel, getPredict

# URL for historical rates
URL_HISTORY = 'https://api.exchangeratesapi.io/history'

# Version 1, set dataset for the amount of 5 years
start_at = (datetime.today() - timedelta(days=365*5)).strftime("%Y-%m-%d")
end_at = datetime.today().strftime("%Y-%m-%d")

URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

# train parameters
seq_length = 50       # sequence length
input_dim = 1          # dimension of input value
output_dim = 1         # dimenstion of output value
learning_rate = 0.01
iterations = 20
size = 0.9 # the portion of the dataset to in the train split

for unit in ['USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW']:
    dataset = getHistoricalDataset(URL, unit)

    dataset_rate = getConvertToArray(dataset)

    train_set, test_set = getTrainTestSplite(dataset_rate, size, seq_length)

    train_set = MinMaxScaler(train_set)
    test_set = MinMaxScaler(test_set)

    X_train, y_train = build_window(train_set, seq_length)
    X_test, y_test = build_window(test_set, seq_length)

    lstm_model = getModel(input_dim, output_dim, seq_length, learning_rate)

    executeTrain(lstm_model, X_train, y_train, iterations)

    evaluateModel(lstm_model, X_test, y_test)

    saveTrainedModel(lstm_model, 'model_' + unit)