import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import datetime
from fbprophet import Prophet


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

def get_last_x(dataset, look_back):
    dataX = []
    a = dataset[(len(dataset) - look_back):len(dataset), 0]
    dataX.append(a)
    dataX = np.array(dataX)
    dataX = np.reshape(dataX, (dataX.shape[0], dataX.shape[1], 1))
    return dataX

def train(dataset, days):
    m = Prophet()
    m.fit(dataset)
    future = m.make_future_dataframe(periods=days)
    forecast = m.predict(future)
    fig = m.plot(forecast)
    fig.show()
    fig = m.plot_components(forecast)
    fig.show()
    return forecast



def predict(days):
    begin_time = datetime.datetime.now()

    # load the dataset
    dataframe = pd.read_pickle('origin_data.pickle').reset_index()
    dataframe.rename(columns={'rq':'ds', 'spj':'y'}, inplace=True)
    future = train(dataframe, days)
    return future

if __name__ == '__main__':
    predict(5)

