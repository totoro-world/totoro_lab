import security
import datetime
import pandas as pd
import shape
import matplotlib.pyplot as plt
import numpy as np
import math_util

class ShapeStgy:
    def __init__(self, sec_pool_list, end_date, shape_period):
        self.shape_period = shape_period
        begin_date = end_date - datetime.timedelta(days=shape_period)
        self.sec_pool_list = []
        for code in sec_pool_list:
            self.sec_pool_list.append(security.Security(code[0], code[1], begin_date, end_date))


    def run(self):
        # load data
        for sec in self.sec_pool_list:
            sec.load_data()

        r = {}
        for i, sec in enumerate(self.sec_pool_list):
            shape_seri = sec.close_price_seri
            shape_ins = shape.Shape(0.05)
            try:
                (shape_id, shape_name) = shape_ins.what_shape(shape_seri)
            except:
                (shape_id, shape_name) = (-1, 'exception')
            if not shape_name in r.keys():
                r[shape_name] = []
            r[shape_name].append((sec.code, sec.name))

        for key in r.keys():
            print('---[{0}]---'.format(key))
            for code in r[key]:
                print('{0} {1}'.format(code[0], code[1]))
