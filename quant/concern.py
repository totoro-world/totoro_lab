import datetime
import simple_stgy
import wind_util

data_period = 90
shape_period = 15
today = datetime.datetime.today()
end_date = today - datetime.timedelta(days=1)
concern_sec_list = ['000300.SH','HSI.HI', '399006.SZ', '000905.SH', '399975.SZ', 'XAUCNY.IDC', '000993.SH']
name_df = wind_util.get_all_index()
concern_sec_list = wind_util.pack_sec_name(concern_sec_list, name_df)

stgy = simple_stgy.SimpleStgy(concern_sec_list, end_date, data_period, shape_period)
stgy.run()


