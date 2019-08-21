import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import datetime
import wind_util

def analysis(period):
    end_date = datetime.datetime.today()
    end_date = end_date - datetime.timedelta(days=1)
    begin_date = end_date - datetime.timedelta(days=period)

    pmi_data = wind_util.get_pmi(begin_date, end_date)
    pmi_data.name = 'pmi'
    pmi_data.plot(title='economy growth')
    plt.show()

    ll_data = wind_util.get_1ygz(begin_date, end_date)
    ll_data.name = 'll'
    ll_data.plot(title='interest rate')
    plt.show()

    xy_data = wind_util.get_1yxy(begin_date, end_date)
    xy_data = xy_data.reindex(ll_data.index, method='backfill')
    xy_data = xy_data - ll_data
    xy_data.name = 'xy'
    xy_data.plot(title='credit')
    plt.show()

    wh_data = wind_util.get_wh(begin_date, end_date)
    wh_data.plot(title='foreign exchange')
    plt.show()


    cpi_data = wind_util.get_cpi(begin_date, end_date)
    #cpi_data.name = 'cpi'
    #cpi_data.plot(title='inflation_cpi')
    #plt.show()

    ppi_data = wind_util.get_ppi(begin_date, end_date)
    #ppi_data.name = 'ppi'
    #ppi_data.plot(title='inflation_ppi')
    #plt.show()
    ppi_data = ppi_data.reindex(cpi_data.index, method='backfill')

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(cpi_data.index, cpi_data.values)
    ax1.set_ylabel('cpi')
    ax1.set_title("inflation")

    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(ppi_data.index, ppi_data.values, 'r')
    ax2.set_ylabel('ppi')
    plt.show()



if __name__ == '__main__':
    analysis(365 * 3)

