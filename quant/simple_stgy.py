import security
import datetime
import pandas as pd
import shape
import matplotlib.pyplot as plt
import numpy as np
import math_util

class SimpleStgy:
    def __init__(self, concern_sec_list, end_date, data_period, shape_period):
        self.shape_period = shape_period
        self.data_period = data_period
        begin_date = end_date - datetime.timedelta(days=data_period)
        self.concern_sec_list = []
        for code in concern_sec_list:
            self.concern_sec_list.append(security.Security(code[0], code[1], begin_date, end_date))

    def cal_seri_indicator(seri):
        df = pd.DataFrame()
        df['value'] = seri
        median = seri.median()
        df['median'] = median
        leastsq = math_util.const_leastsq([median], seri.index, seri.values)
        df['leastsq'] = leastsq
        return df

    def run(self):
        # load data
        for sec in self.concern_sec_list:
            sec.load_data()

        fig, axes = plt.subplots(len(self.concern_sec_list), 1, figsize=(20, 40))
        for i, sec in enumerate(self.concern_sec_list):
            # cal shape
            print('[{0} {1}]'.format(sec.code, sec.name))
            shape_seri = sec.close_price_seri[-self.shape_period:]
            #print(shape_seri)
            print('yesterday price:{0}'.format(shape_seri[-1]))
            shape_ins = shape.Shape(0.05)
            (shape_id, shape_name) = shape_ins.what_shape(shape_seri)
            print("shape:{0}".format(shape_name))

            # draw k
            spot_seri = sec.close_price_seri
            spot_df = SimpleStgy.cal_seri_indicator(spot_seri)
            spot_df.plot(ax=axes[i], title='{0} {1}, days({2})'.format(sec.code, sec.name, self.data_period))
        fig.subplots_adjust(top=0.97, bottom=0.05, left=0.04, right=0.97, hspace=0, wspace=0)
        plt.show()
