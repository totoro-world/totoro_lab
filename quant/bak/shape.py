class Shape():
    def __init__(self, delta_percent):
        self.delta_percent = delta_percent
        self.kShape_list = [{'name': 'y_mirror_tick', 'func': self.is_y_mirror_tick},
                            {'name': 'x_mirror_tick', 'func': self.is_x_mirror_tick},
                            {'name': 'tick', 'func': self.is_tick},
                            {'name': 'clockwise_180_tick', 'func': self.is_clockwise_180_tick},
                            {'name': 'up_line', 'func': self.is_up_line},
                            {'name': 'down_line', 'func': self.is_down_line},
                            {'name': 'up_arrow', 'func': self.is_up_arrow},
                            {'name': 'down_arrow', 'func': self.is_down_arrow}]

    def is_down_arrow(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]

        if (min_date > max_date
            and last_price > min_price):
            return True

        return False

    def is_up_arrow(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]

        if (max_date > min_date
            and last_price < max_price):
            return True

        return False

    def is_y_mirror_tick(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]

        if not self.is_down_arrow(price_series):
            return False

        # this is for sure we can own at least delta_percent profit
        if max_price > last_price * (1 + self.delta_percent):
            return True

        return False

    def is_tick(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]
        first_price = price_series.iloc[0]

        if not self.is_down_arrow(price_series):
            return False

        # this is for sure we can own at least delta_percent profit
        if max_price > first_price * (1 + self.delta_percent):
            return True

        return False

    def is_clockwise_180_tick(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]

        if not self.is_up_arrow(price_series):
            return False

        # this is for sure we may loss at least delta_percent profit
        if last_price > min_price * (1 + self.delta_percent):
            return True

        return False

    def is_x_mirror_tick(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]
        first_price = price_series.iloc[0]

        if not self.is_up_arrow(price_series):
            return False

        # this is for sure we may loss at least delta_percent profit
        if first_price > min_price * (1 + self.delta_percent):
            return True

        return False

    def is_up_line(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]

        if (max_date > min_date
            and max_price == last_price):
            return True

        return False

    def is_down_line(self, price_series):
        min_price = price_series.min()
        max_price = price_series.max()
        min_date = price_series.idxmin()
        max_date = price_series.idxmax()
        last_price = price_series.iloc[-1]

        if (min_date > max_date
            and min_price == last_price):
            return True

        return False

    def what_shape(self, price_series):
        for i in range(0, len(self.kShape_list)):
            shape_define = self.kShape_list[i]
            if shape_define['func'](price_series):
                return (i, shape_define['name'])

        return (-1, 'unknown')

