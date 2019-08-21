from WindPy import *
import pandas as pd
import datetime

w.start()

# 通胀
def get_cpi(begin_date, end_date):
    data = get_ebd('M0043747', begin_date, end_date)
    return data

def get_ppi(begin_date, end_date):
    data = get_ebd('M5567965', begin_date, end_date)
    return data

# 经济增长
def get_pmi(begin_date, end_date):
    data = get_ebd('M0017126', begin_date, end_date)
    return data

def get_ebd(code, begin_date, end_date):
    data = w.edb(code, begin_date, end_date, 'Fill=Previous')
    seri = pd.Series(data.Data[0], index=data.Times)
    return seri

# 利率
def get_1ygz(begin_date, end_date):
    data = w.wsd("TB1Y.WI", "close", begin_date, end_date, "PriceAdj=YTM")
    seri = pd.Series(data.Data[0], index=data.Times)
    return seri

# 信用
def get_1yxy(begin_date, end_date):
    data = w.wsd("CRAIL1Y.WI", "close", begin_date, end_date, "PriceAdj=YTM")
    seri = pd.Series(data.Data[0], index=data.Times)
    return seri

# 外汇
def get_wh(begin_date, end_date):
    data = w.wsd("USDCNY.EX", "close", begin_date, end_date, "")
    seri = pd.Series(data.Data[0], index=data.Times)
    return seri




