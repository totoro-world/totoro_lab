import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split
import datetime
from sklearn import metrics
import xgboost as xgb


def prepare_data(df, shift_days):
    res = df.copy()
    for i in range(0, shift_days):
        s = df.shift((i + 1))
        res = pd.merge(res, s, how='left', left_index=True, right_index=True, suffixes=('', str(i + 1)))

    res = res.iloc[shift_days:]
    return res

def train(df, show_plot=False):
    # fix random seed for reproducibility
    np.random.seed(7)

    # split x, y
    x_df = df.iloc[:, 1:]
    y_df = df.iloc[:, 0]

    # split train test 
    x_train, x_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.2, random_state=100)

	# xgboost model
    xg_reg = xgb.XGBRegressor(objective='reg:linear',
                              colsample_bytree=0.3,
                              learning_rate=0.1,
                              max_depth=5,
                              alpha=10,
                              n_estimators=10)
    xg_reg.fit(x_train, y_train)
    y_predict = xg_reg.predict(x_test)

    if show_plot:
        xgb.plot_importance(xg_reg)
        plt.show()

    # predict next y
    next_x = df.iloc[-1, 0:(len(df.columns) - 1)]
    next_x = pd.DataFrame().append(next_x.to_dict(), ignore_index=True)
    col_rename_dict = dict(zip(next_x.columns, x_df.columns))
    next_x.rename(columns=col_rename_dict, inplace=True)
    next_y = xg_reg.predict(next_x)

    return next_y[0]

def predict(days):
    begin_time = datetime.datetime.now()

    # load the dataset
    origin_df = pd.read_pickle('origin_data.pickle')

    predict_df = pd.DataFrame()
    for i in range(0, days):
        print('### {0} left ###'.format(days - i))
        # train
        df = pd.concat([origin_df, predict_df], ignore_index=True)
        df = prepare_data(df, 3)
        next_y = train(df)
        predict_df = predict_df.append({origin_df.columns[0]:next_y}, ignore_index=True)

    # finish train
    end_time = datetime.datetime.now()
    print('total cost time: {0} minites'.format((end_time - begin_time).seconds // 60))

    # plot result
    plt.plot(origin_df.values)
    predict_plot = pd.concat([origin_df, predict_df], ignore_index=True).values
    predict_plot[0:origin_df.shape[0], :] = np.nan
    plt.plot(predict_plot)
    plt.show()

if __name__ == '__main__':
    predict(30)

