import datetime
import rtm_stgy
import wind_util

today = datetime.datetime.today()
end_date = today - datetime.timedelta(days=1)
sec_pool_list = ['399975.SZ']
sec_pool_list = [x for x in sec_pool_list if not x.endswith('CSI')]
sec_pool_list = list(set(sec_pool_list))
df = wind_util.get_all_index()
sec_pool_list = wind_util.pack_sec_name(sec_pool_list, df)
sec = sec_pool_list[0]
stgy = rtm_stgy.RtmStgy(sec, end_date, 360)
(max_row, min_row) = stgy.run()










