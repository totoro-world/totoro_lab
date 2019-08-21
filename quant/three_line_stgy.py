import datetime
import pandas as pd
import shape
import matplotlib.pyplot as plt
import numpy as np
import math_util
import wind_util
import security

# 三线模型
class ThreeLineStgy:
    def __init__(self, target_sec, end_date, period_list=[10, 30, 360], show=True):
        self.show = show
        self.period_list = period_list
        begin_date = end_date - datetime.timedelta(days=max(self.period_list))
        self.target_sec = security.Security(target_sec[0], target_sec[1], begin_date, end_date)
        
    def screen_print(self, s):
        if self.show:
            print(s)

    def run(self):
        self.target_sec.load_data()

        self.screen_print('---{0} {1}---'.format(self.target_sec.code, self.target_sec.name))
        self.screen_print('[info]')
        yesterday_price = self.target_sec.close_price_seri[-1]
        self.screen_print('yesterday price:{0}'.format(self.target_sec.close_price_seri[-1]))

        result = pd.DataFrame(columns=['buy_profit', 'shape'])

        # cal three line
        df = pd.DataFrame()
        df['value'] = self.target_sec.close_price_seri
        for period in self.period_list:
            seri = self.target_sec.close_price_seri[-period:]
            median = seri.median()
            leastsq = math_util.const_leastsq([median], seri.index, seri.values)
            df['{0}'.format(period)] = leastsq
            buy_profit = (leastsq - yesterday_price) / yesterday_price * 100
            self.screen_print('{0} price:{1}, buy_profit:{2:.2f}%'.format(period, leastsq, buy_profit))
            result.loc[period, 'buy_profit'] = buy_profit
        if self.show:
            plt.figure()
            df.plot()
            plt.show()

        # cal shape
        self.screen_print('[shape]')
        for period in self.period_list:
            seri = self.target_sec.close_price_seri[-period:]
            shape_ins = shape.Shape(0.05)
            (shape_id, shape_name) = shape_ins.what_shape(seri)
            self.screen_print("{0}:{1}".format(period, shape_name))
            result.loc[period, 'shape'] = shape_name

        # analysis
        self.screen_print('[analysis]')
        def adjust_profit(row):
            if row['shape'] in ('up_line', 'down_line'):
                row['buy_profit'] = 0
            return row
        result = result.apply(adjust_profit, axis=1)
        max_id = result['buy_profit'].idxmax()
        min_id = result['buy_profit'].idxmin()
        latest_id = min(result.index)
        max_row = result.loc[max_id]
        min_row = result.loc[min_id]
        latest_row = result.loc[latest_id]
        self.screen_print('latest: shape({0}, day({1}))'.format(latest_row['shape'], latest_id))
        self.screen_print('max profit: profit({0:.2f}%) shape({1}) day({2})'.format(max_row['buy_profit'], max_row['shape'], max_id))
        self.screen_print('min profit: profit({0:.2f}%) shape({1}) day({2})'.format(min_row['buy_profit'], min_row['shape'], min_id))
        return (latest_row, max_row, min_row)






