from WindPy import *
import datetime
import pandas as pd
import shape
import matplotlib.pyplot as plt
import numpy as np
import math_util
import wind_util
import security
import webbrowser
from statsmodels.tsa.stattools import adfuller

class ValueStgy:
    def __init__(self, target_sec, cor_sec_list, end_date,
                 data_period, correlation_period, shape_period,
                 ic_pvalue = 0.05, adf_pvalue=0.05):
        self.shape_period = shape_period
        self.data_period = data_period
        self.correlation_period = correlation_period
        self.ic_pvalue = ic_pvalue
        self.adf_pvalue = adf_pvalue
        begin_date = end_date - datetime.timedelta(days=data_period)
        self.target_sec = security.Security(target_sec, begin_date, end_date)
        self.cor_sec_list = []
        for sec in cor_sec_list:
            self.cor_sec_list.append(security.Security(sec, begin_date, end_date))

    def value_analyse(self, sec):
        # cal spot indicator
        # cal shape
        print('[{0}]'.format(sec.code))
        shape_seri = sec.close_price_seri[-self.shape_period:]
        print('yesterday price:{0}'.format(shape_seri[-1]))
        shape_ins = shape.Shape(0.05)
        (shape_id, shape_name) = shape_ins.what_shape(shape_seri)
        print("shape:{0}".format(shape_name))
        # draw all spot
        fig, axes = plt.subplots(4, 1, figsize=(20, 40))
        for i in range(0, 4):
            days = self.data_period // 4 * (i + 1)
            spot_seri = sec.close_price_seri.iloc[-days:]
            spot_df = ValueStgy.cal_seri_indicator(spot_seri)

            if shape_seri[-1] > spot_df['leastsq'].iloc[0]:
                signal = '↓'
            elif shape_seri[-1] < spot_df['leastsq'].iloc[0]:
                signal = '↑'
            else:
                signal = '-'
            print('[days:{0}]'.format(days))
            print('median:{0}, leastsq:{1}, signal:{2}'.format(spot_df['median'].iloc[0],
                                                               spot_df['leastsq'].iloc[0],
                                                               signal))
            spot_df.plot(ax=axes[i], title='{0}, days({1})'.format(spot_seri.name, days))
        fig.subplots_adjust(top=0.97, bottom=0.05, left=0.04, right=0.97, hspace=0, wspace=0)

    def load_base_data(self, sec):
        wind_util.fill_close_price(w, sec)
        sec.fill_close_pct_change()
        sec.close_price_median = sec.close_price_seri.median()

    @staticmethod
    def adjust_close_price(seri):
        adjust_seri = (seri - seri.iloc[0]) / abs(seri.iloc[0])
        return adjust_seri

    @staticmethod
    def cal_seri_indicator(seri):
        df = pd.DataFrame()
        df['value'] = seri
        median = seri.median()
        df['median'] = median
        leastsq = math_util.const_leastsq([median], seri.index, seri.values)
        df['leastsq'] = leastsq
        return df

    def cal_delta_seri(self, sec):
        target_close_price_seri = ValueStgy.adjust_close_price(self.target_sec.close_price_seri.iloc[-self.correlation_period:])
        sec_close_price_seri = ValueStgy.adjust_close_price(sec.close_price_seri.iloc[-self.correlation_period:])
        # adjust to same distance
        target_delta_area = target_close_price_seri.max() - target_close_price_seri.min()
        sec_delta_area = sec_close_price_seri.max() - sec_close_price_seri.min()
        amf_cor = sec_delta_area / target_delta_area
        target_close_price_seri = target_close_price_seri * amf_cor
        if (sec.ic > 0):
            delta_seri = target_close_price_seri - sec_close_price_seri
        else:
            delta_seri = target_close_price_seri + sec_close_price_seri
        df = ValueStgy.cal_seri_indicator(delta_seri)
        leastsq = df['leastsq'].iloc[0]
        df['target'] = target_close_price_seri
        df['security'] = sec_close_price_seri
        return df

    def cointegration_analyse(self):
        print('------cointegration analyse days({0})'.format(self.correlation_period))
        for sec in self.cor_sec_list:
            sec.delta_df = self.cal_delta_seri(sec)
            sec.adf, sec.adf_pvalue = math_util.adf_test(sec.delta_df['value'].values)
            print('{0}: adf({1}), p_value({2})'.format(sec.code, sec.adf, sec.adf_pvalue))


        df = pd.DataFrame()
        df['sec'] = [sec for sec in self.cor_sec_list if sec.adf_pvalue < self.adf_pvalue]
        df['adf'] = [sec.adf for sec in self.cor_sec_list if sec.adf_pvalue < self.adf_pvalue]
        df.sort_values('adf', inplace=True, ascending=False)

        if df.shape[0] != 0:
            fig, axes = plt.subplots(df.shape[0], 1, sharex=True, figsize=(20, 40))
            for i in range(0, df.shape[0]):
                sec = df.iloc[i]['sec']
                sec.delta_df.plot(axes[i], sec.code)
            fig.subplots_adjust(top=0.97, bottom=0.05, left=0.04, right=0.97, hspace=0, wspace=0)

    def correlation_analyse(self):
        print('------correlation analyse days({0})'.format(self.correlation_period))
        for sec in self.cor_sec_list:
            sec.ic, sec.ic_pvalue = math_util.SpearmanIC(
                self.target_sec.close_pct_change_seri[-self.correlation_period:],
                sec.close_pct_change_seri[-self.correlation_period:])
            print('{0}: ic({1:.2f}), p_value({2:.2f})'.format(sec.code, sec.ic, sec.ic_pvalue))

        df = pd.DataFrame()
        df['sec'] = [sec for sec in self.cor_sec_list if sec.ic_pvalue < self.ic_pvalue]
        df['ic'] = [sec.ic for sec in self.cor_sec_list if sec.ic_pvalue < self.ic_pvalue]
        df.sort_values('ic', inplace=True, ascending=False)

        for i in range(0, df.shape[0]):
            sec = df.iloc[i]['sec']
            self.value_analyse(sec)

    def run(self, show_fig=True):
        w.start()

        # load target sec data
        self.load_base_data(self.target_sec)

        # load correlation sec data
        for sec in self.cor_sec_list:
            self.load_base_data(sec)


        # target value analyse
        print('------value analyse')
        self.value_analyse(self.target_sec)

        # correlation analyse
        self.correlation_analyse()

        # cointegration analyse
        self.cointegration_analyse()

        if (show_fig):
            plt.show()

        w.stop()


