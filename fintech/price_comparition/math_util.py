from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
import numpy as np
import numpy.random as nrand
from scipy import optimize
from statsmodels.tsa.stattools import adfuller

# stock_return = [], factor_value = []  or series
def PearsonIC(stock_return, factor_value):
    return pearsonr(stock_return, factor_value)

# stock_return = [], factor_value = [] or series
def SpearmanIC(stock_return, factor_value):
    return spearmanr(stock_return, factor_value)

# stock_return = [], factor_value = [] or series
def SpearmanRandIC(stock_return, factor_value):
    sort_stock_return = stock_return[:]
    sort_stock_return.sort()
    sort_factor_value = factor_value[:]
    sort_factor_value.sort()
    rank_stock_return = [ sort_stock_return.index(i) for i in stock_return ]
    rank_factor_value = [ sort_factor_value.index(i) for i in factor_value ]
    return spearmanr(rank_stock_return, rank_factor_value)

def const_leastsq(ref_value_list, x_list, y_list):
    def leastsq_func(x, p):
        a = p[0]
        return a

    def leastsq_residuals(p, x, y):
        return leastsq_func(x, p) - y

    r = optimize.leastsq(leastsq_residuals, ref_value_list, args=(x_list, y_list))
    return r[0][0]

def adf_test(x, regression='c'):
    re = adfuller(x, regression=regression)
    return (re[0], re[1])
