import wind_util

class Security():
    def __init__(self, code, name, begin_date, end_date):
        self.code = code
        self.name = name
        self.begin_date = begin_date
        self.end_date = end_date
        self.close_price_seri = None
        self.close_pct_change_seri = None

    def load_data(self):
        wind_util.fill_close_price(self)

    def fill_close_pct_change(self):
        self.close_pct_change_seri = self.close_price_seri.pct_change().iloc[1:]

