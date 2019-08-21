import wind_util
import datetime

def fetch_gold_data():
    end_date = datetime.datetime.today()
    data_spread = 1 * 365
    begin_date = end_date - datetime.timedelta(days=data_spread)
    seri = wind_util.get_close_price('SPTAUUSDOZ.IDC', begin_date, end_date) #SPTAUUSDOZ.IDC
    df = seri.to_frame()
    df.to_pickle('origin_data.pickle')

if __name__ == '__main__':
    fetch_gold_data()
