import wind_util
import datetime

def fetch_data():
    end_date = datetime.datetime.today()
    data_spread = 1 * 365
    begin_date = end_date - datetime.timedelta(days=data_spread)
    seri = wind_util.get_close_price('USDX.FX', begin_date, end_date)
    df = seri.to_frame()
    df.to_pickle('origin_data.pickle')

if __name__ == '__main__':
    fetch_data()
