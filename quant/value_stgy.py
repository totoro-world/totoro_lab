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
import statsmodels.api as sm

def print_quant_ret(quant_ret):
    total_sum = sum(quant_ret)
    if total_sum != 0:
        print('↑:{0:.2f}, -:{1:.2f}, ↓:{2:.2f}, origin data:{3}'.format(
            quant_ret[0] / total_sum, quant_ret[1] / total_sum, quant_ret[2] / total_sum,
            quant_ret))

class ValueStgy:
    def __init__(self, target_sec, cor_sec_list, end_date,
                 data_period, correlation_period, shape_period,
                 adf_pvalue = 0.05):
        self.ic_pvalue = 0.05
        self.ic_value = 0.4 #0.8强相关，0.5-0.8显著相关， 0.3-0.5弱相关， 0.3不相关
        self.adf_pvalue = adf_pvalue

        self.shape_period = shape_period
        self.data_period = data_period
        self.correlation_period = correlation_period
        begin_date = end_date - datetime.timedelta(days=data_period)
        self.target_sec = security.Security(target_sec, 'gold', begin_date, end_date)
        self.cor_sec_list = []
        for sec in cor_sec_list:
            sec_ins = security.Security(sec, '', begin_date, end_date)
            self.cor_sec_list.append(sec_ins)

    def value_analyse(self, sec):
        quant_ret = [0, 0, 0]
        # cal spot indicator
        # cal shape
        print('[{0}]'.format(sec.code))
        shape_seri = sec.close_price_seri[-self.shape_period:]
        #print(shape_seri)
        print('yesterday price:{0}'.format(shape_seri[-1]))
        shape_ins = shape.Shape(0.05)
        (shape_id, shape_name) = shape_ins.what_shape(shape_seri)
        print("shape:{0}".format(shape_name))
        profit_list = []
        # draw all spot
        period_list = [360, 180, 90, 30, 7]
        fig, axes = plt.subplots(len(period_list), 1, figsize=(20, 40))
        regime_list = []
        for i in range(0, len(period_list)):
            days = period_list[i]
            spot_seri = sec.close_price_seri.iloc[-days:]
            spot_df = ValueStgy.cal_seri_indicator(spot_seri)
            profit = spot_df['leastsq'].iloc[0] - shape_seri[-1]
            profit_list.append(profit)
            regime_list.append(spot_df['leastsq'].iloc[0])
            if shape_seri[-1] > spot_df['leastsq'].iloc[0]:
                signal = '↓'
                quant_ret[2] += 1
            elif shape_seri[-1] < spot_df['leastsq'].iloc[0]:
                signal = '↑'
                quant_ret[0] += 1
            else:
                signal = '-'
                quant_ret[1] += 1
            print('[days:{0}]'.format(days))
            print('median:{0}, leastsq:{1}, signal:{2}, profit:{3}'.format(spot_df['median'].iloc[0],
                                                                           spot_df['leastsq'].iloc[0],
                                                                           signal,
                                                                           profit))
            spot_df.plot(ax=axes[i], title='{0}, days({1})'.format(spot_seri.name, days))
        fig.subplots_adjust(top=0.97, bottom=0.05, left=0.04, right=0.97, hspace=0, wspace=0)
        print('profit: min({0}), max({1})'.format(min(profit_list), max(profit_list)))

        # regime shape
        print("[regime shape]")
        regime_seri = pd.Series(regime_list)
        (shape_id, shape_name) = shape_ins.what_shape(regime_seri)
        print("shape:{0}".format(shape_name))
        return quant_ret

    def load_base_data(self, sec):
        wind_util.fill_close_price(sec)
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

    def cal_spread_seri(self, sec):
        target_seri = self.target_sec.close_price_seri.iloc[-self.correlation_period:]
        sec_seri = sec.close_price_seri.iloc[-self.correlation_period:]

        # eg test
        adf, adf_pvalue = math_util.adf_test(target_seri.diff()[1:], regression='ct')
        if adf_pvalue > self.adf_pvalue:
            print('{0} one degree diff not stationary'.format(self.target_sec.code))
            return None

        adf, adf_pvalue = math_util.adf_test(sec_seri.diff()[1:], regression='ct')
        if adf_pvalue > self.adf_pvalue:
            print('{0} one degree diff not stationary'.format(sec.code))
            return None

        # ols
        y = target_seri.values
        x = sec_seri.values
        nx = sm.add_constant(x)
        est = sm.OLS(y, nx)
        est = est.fit()
        test_re = sm.stats.linear_rainbow(est)
        a = est.params[0]
        b = est.params[1]
        print('code({0}) linear regression(pvalue:{3}), param: a({1}), b({2})'.format(sec.code, a, b, test_re[1]))
        x = a + b * x
        spread = y - x

        spread_seri = pd.Series(data=spread, index=target_seri.index)
        sec.adf, sec.adf_pvalue = math_util.adf_test(spread_seri.values, regression='ct')
        if sec.adf_pvalue > self.adf_pvalue:
            print('{0}: adf({1}), p_value({2}) adf test fail'.format(sec.code, sec.adf, sec.adf_pvalue))
            return None
        else:
            print('{0}: adf({1}), p_value({2}) adf test pass'.format(sec.code, sec.adf, sec.adf_pvalue))

        target_seri = pd.Series(data=y, index=target_seri.index)
        sec_seri = pd.Series(data=x, index=sec_seri.index)
        df = ValueStgy.cal_seri_indicator(spread_seri)
        leastsq = df['leastsq'].iloc[0]
        return df


    def print_cointegration_info(self, sec, quant_ret):
        spread_df = sec.spread_df
        target_signal = ''
        sec_signal = ''
        spread_signal = ''
        current_value = spread_df['value'].iloc[-1]
        base_value = spread_df['leastsq'].iloc[0]
        if current_value > base_value:
            spread_signal = '↓'
            target_signal = '↓'
            quant_ret[2] += 1
            if sec.ic >= 0:
                sec_signal = '↑'
            else:
                sec_signal = '↓'
        elif current_value < base_value:
            spread_signal = '↑'
            target_signal = '↑'
            quant_ret[0] += 1
            if sec.ic >= 0:
                sec_signal = '↓'
            else:
                sec_signal = '↑'
        else:
            spread_signal = '-'
            target_signal = '-'
            sec_signal = '-'
            quant_ret[1] += 1
        print('signal: current({0}), base({1}), spread({2}) so {3}({4}) or {5}({6})'.format(current_value, base_value, spread_signal,
                                                                                            self.target_sec.code, target_signal, sec.code, sec_signal))


    def cointegration_analyse(self):
        quant_ret = [0, 0, 0]
        print('------cointegration analyse days({0})'.format(self.correlation_period))
        for sec in self.cor_sec_list:
            sec.spread_df = self.cal_spread_seri(sec)

        print('[signal report]')
        df = pd.DataFrame()
        l = [(sec, sec.adf) for sec in self.cor_sec_list if sec.spread_df is not None and sec.adf_pvalue <= self.adf_pvalue]
        l = list(map(list, zip(*l)))
        if len(l) != 0:
            df['sec'] = l[0]
            df['adf'] = l[1]
            df.sort_values('adf', inplace=True, ascending=True)

        if df.shape[0] >= 2:
            fig, axes = plt.subplots(df.shape[0], 1, figsize=(20, 40))
            for i in range(0, df.shape[0]):
                sec = df.iloc[i]['sec']
                sec.spread_df.plot(ax=axes[i], title=sec.code)
                self.print_cointegration_info(sec, quant_ret)
            fig.subplots_adjust(top=0.97, bottom=0.05, left=0.04, right=0.97, hspace=0, wspace=0)
        elif df.shape[0] == 1:
            fig = plt.figure(figsize=(20, 40))
            ax = fig.add_axes([0, 0, 1, 1])
            sec = df.iloc[0]['sec']
            sec.spread_df.plot(ax=ax, title=sec.code)
            self.print_cointegration_info(sec, quant_ret)
            fig.subplots_adjust(top=0.97, bottom=0.05, left=0.04, right=0.97, hspace=0, wspace=0)

        return quant_ret

    def correlation_analyse(self):
        quant_ret = [0, 0, 0]
        print('------correlation analyse days({0})'.format(self.correlation_period))
        for sec in self.cor_sec_list:
            sec.ic, sec.ic_pvalue = math_util.SpearmanIC(
                self.target_sec.close_pct_change_seri[-self.correlation_period:],
                sec.close_pct_change_seri[-self.correlation_period:])
            print('{0}: ic({1:.2f}), p_value({2})'.format(sec.code, sec.ic, sec.ic_pvalue))

        df = pd.DataFrame()
        l = [(sec, sec.ic) for sec in self.cor_sec_list if sec.ic_pvalue <= self.ic_pvalue and abs(sec.ic) >= self.ic_value]
        l = list(map(list, zip(*l)))
        if len(l) != 0:
            df['sec'] = l[0]
            df['ic'] = l[1]
            df.sort_values('ic', inplace=True, ascending=False)

        print('*** positive security')
        positive_df = df[df.ic >= 0]
        for i in range(0, positive_df.shape[0]):
            sec = positive_df.iloc[i]['sec']
            print('{0}: ic({1})'.format(sec.code, sec.ic))
            q_r = self.value_analyse(sec)
            quant_ret = [sum(x) for x in zip(quant_ret, q_r)]

        print('*** negative security')
        negative_df = df[df.ic < 0]
        for i in range(0, negative_df.shape[0]):
            sec = negative_df.iloc[i]['sec']
            print('{0}: ic({1})'.format(sec.code, sec.ic))
            q_r = self.value_analyse(sec)
            q_r = [q_r[2], q_r[1], q_r[0]]
            quant_ret = [sum(x) for x in zip(quant_ret, q_r)]

        return quant_ret

    def run(self, show_fig=True):
        # load target sec data
        self.load_base_data(self.target_sec)

        # load correlation sec data
        for sec in self.cor_sec_list:
            self.load_base_data(sec)
            sec.close_price_seri = sec.close_price_seri.reindex(
                self.target_sec.close_price_seri.index,
                method='nearest')

        # target value analyse
        print('------value analyse')
        value_quant = self.value_analyse(self.target_sec)

        # correlation analyse
        correlation_quant = self.correlation_analyse()

        # cointegration analyse
        cointegration_quant = self.cointegration_analyse()

        if (show_fig):
            plt.show()

        return (value_quant, correlation_quant, cointegration_quant)



