import datetime
import pandas as pd
import shape
import matplotlib.pyplot as plt
import numpy as np
import math_util
import wind_util
import security

# 三线模型的进化版
class RtmStgy:
    def __init__(self, target_sec, end_date, period, change_percent=0.01, regime_percent=0.05, regime_tp_num=4, show=True):
        self.show = show
        self.period = period
        self.change_percent = change_percent
        self.regime_percent = regime_percent
        self.regime_tp_num = regime_tp_num
        begin_date = end_date - datetime.timedelta(days=self.period)
        self.target_sec = security.Security(target_sec[0], target_sec[1], begin_date, end_date)

    def screen_print(self, s):
        if self.show:
            print(s)

    def run(self):
        self.target_sec.load_data()
        seri = self.target_sec.close_price_seri

        # basic info
        self.screen_print('---{0} {1}---'.format(self.target_sec.code, self.target_sec.name))
        self.screen_print('[info]')
        yesterday_price = self.target_sec.close_price_seri[-1]
        self.screen_print('yesterday price:{0}'.format(self.target_sec.close_price_seri[-1]))

        # dynamic cal tp
        df = pd.DataFrame()
        df['price'] = self.target_sec.close_price_seri
        result = pd.DataFrame(columns=['profit'])
        tp_df = pd.DataFrame()
        tp_seri = pd.Series()
        regime_tp_list = []
        # temp var
        last_tp = None
        candidate_tp = None
        regime_tp_num = 0
        max_regime_tp = None
        min_regime_tp = None
        tp_win_list = []
        for i, (rq, price) in enumerate(seri.iteritems()):
            point = {'idx':i , 'rq':rq, 'price':price, 'pct':0}
            if last_tp is None:
                last_tp = point
                regime_tp_list.append(point)
                continue

            percent_to_turn = (point['price'] - last_tp['price']) / last_tp['price']
            point['pct'] = percent_to_turn
            if candidate_tp is None:
                # find the first candidate
                if percent_to_turn >= self.change_percent or percent_to_turn <= -self.change_percent:
                    candidate_tp = point
                continue

            is_up_trend = (candidate_tp['pct'] >= 0 and percent_to_turn > candidate_tp['pct'])
            is_down_trend = (candidate_tp['pct'] <= 0 and percent_to_turn < candidate_tp['pct'])
            if is_up_trend or is_down_trend:
                candidate_tp = point
            else:
                percent_to_candidate = (point['price'] - candidate_tp['price']) / candidate_tp['price']
                if percent_to_candidate < self.change_percent and percent_to_candidate > -self.change_percent:
                    continue

                # regime shift
                if max_regime_tp is not None:
                    percent_to_max = abs((point['price'] - max_regime_tp['price']) / max_regime_tp['price'])
                else:
                    percent_to_max = 0
                if min_regime_tp is not None:
                    percent_to_min = abs((point['price'] - min_regime_tp['price']) / min_regime_tp['price'])
                else:
                    percent_to_min = 0
                if percent_to_max > self.regime_percent or percent_to_min > self.regime_percent:
                    # cal profit
                    head_tp = regime_tp_list[-1]
                    tail_tp = last_tp
                    if head_tp['idx'] != tail_tp['idx']:
                        win_seri = seri[head_tp['idx']:tail_tp['idx']]
                        # if window seri change between regime_percent
                        if (regime_tp_num >= self.regime_tp_num):
                            median = win_seri.median()
                            leastsq = math_util.const_leastsq([median], win_seri.index, win_seri.values)
                            days = (tail_tp['rq'] - head_tp['rq']).days
                            period = '{0}<-{2}->{1}'.format(head_tp['rq'], tail_tp['rq'], days)
                            df[period] = leastsq
                            df[period+'_'] = win_seri
                            tp_win_list.append(win_seri)
                            profit = (leastsq - yesterday_price) / yesterday_price * 100
                            self.screen_print('{0}: price({1}), profit({2:.2f}%)'.format(period, leastsq, profit))
                            result.loc[period, 'profit'] = profit

                    # print('rtl append {0}'.format(point))
                    regime_tp_list.append(point)
                    # clear regime tp
                    # print('--------- regime end-------')
                    regime_tp_num = 0
                    max_regime_tp = None
                    min_regime_tp = None

                # new tp
                # filter non regime tp
                if len(regime_tp_list) == 0 or regime_tp_list[-1]['idx'] <= last_tp['idx']:
                    # print('regime tp {0} {1} {2}'.format(last_tp['rq'], last_tp['price'], regime_tp_num))
                    regime_tp_num += 1
                    if max_regime_tp is None or last_tp['price'] > max_regime_tp['price']:
                        max_regime_tp = last_tp
                    if min_regime_tp is None or last_tp['price'] < min_regime_tp['price']:
                        min_regime_tp = last_tp
                tp_seri.loc[last_tp['rq']] = last_tp['price']
                last_tp = candidate_tp
                point['pct'] = percent_to_candidate
                candidate_tp = point



        # process final tp
        tp_seri.loc[last_tp['rq']] = last_tp['price']
        if candidate_tp is not None:
            tp_seri.loc[candidate_tp['rq']] = candidate_tp['price']

        # draw result
        if self.show:
            df.plot()

        # draw tp
        tp_df['price'] = tp_seri
        for x, y in enumerate(tp_win_list):
            tp_df[str(x)] = y
        if self.show:
            tp_df.plot()

        # analysis
        self.screen_print('[analysis]')
        max_id = result['profit'].idxmax()
        min_id = result['profit'].idxmin()
        max_row = result.loc[max_id]
        min_row = result.loc[min_id]
        self.screen_print('max profit: profit({0:.2f}%) day({1})'.format(max_row['profit'],  max_id))
        self.screen_print('min profit: profit({0:.2f}%) day({1})'.format(min_row['profit'],  min_id))

        # draw at the end
        if self.show:
            plt.show()
        return (max_row, min_row)






