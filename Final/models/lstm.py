# from keras.models import Sequential
# from keras.layers import Embedding, SimpleRNN

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

import requests
from datetime import datetime, timedelta 

# URL for historical rates
URL_HISTORY = 'https://api.exchangeratesapi.io/history'

# Version 1, set dataset for the amount of 3 years
start_at = (datetime.today() - timedelta(days=365*3)).strftime("%Y-%m-%d")
end_at = datetime.today().strftime("%Y-%m-%d")

URL = URL_HISTORY + '?start_at=' + start_at + '&end_at=' + end_at

response = requests.get(URL)
json = response.json()
json = json['rates'].items()

rates = {}
for key, value in sorted(json):
    # print(str(key) + '=>' + str(value))
    rates[key] = value['KRW']

