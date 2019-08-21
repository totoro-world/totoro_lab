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

def train(dataset, look_back, show_plot=False):
    # fix random seed for reproducibility
    np.random.seed(7)
    # normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    # split into train and test sets
    train_size = int(len(dataset) * 0.67)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    # reshape into X=t and Y=t+1
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(4, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=50, batch_size=1, verbose=2)
    # make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    # invert predictions
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])
    # calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    print('Test Score: %.2f RMSE' % (testScore))
    # shift train predictions for plotting
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict
    if show_plot:
        # plot baseline and predictions
        plt.plot(scaler.inverse_transform(dataset))
        plt.plot(trainPredictPlot)
        plt.plot(testPredictPlot)
        plt.show()
    # predict next y
    next_x = get_last_x(dataset, look_back)
    next_y = model.predict(next_x)
    next_y = scaler.inverse_transform(next_y)
    return model, next_y


def predict(days):
    begin_time = datetime.datetime.now()

    # load the dataset
    dataframe = pd.read_pickle('origin_data.pickle')
    dataset = dataframe.values
    dataset = dataset.astype('float32')

    # time window
    look_back = 3

    predict_result = None
    for i in range(0, days):
        print('### {0} left ###'.format(days - i))
        # train
        if predict_result is None:
            model, next_y = train(dataset, look_back)
            predict_result = next_y
        else:
            model, next_y = train(np.append(dataset, predict_result, axis=0), look_back)
            predict_result = np.append(predict_result, next_y, axis=0)

    # finish train
    end_time = datetime.datetime.now()
    print('total cost time: {0} minites'.format((end_time - begin_time).seconds // 60))

    # plot result
    plt.plot(dataset)
    predict_plot = np.append(dataset, predict_result, axis=0)
    predict_plot[0:len(dataset), :] = np.nan
    plt.plot(predict_plot)
    plt.show()

if __name__ == '__main__':
    predict(5)

