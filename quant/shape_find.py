import datetime
import shape_stgy
import wind_util


shape_period = 60
today = datetime.datetime.today()
end_date = today - datetime.timedelta(days=1)
sec_pool_list = (['000918.SH', '000919.SH', '000951.SH', '399905.SZ', '000951.SH', '399975.SZ', 'XAUCNY.IDC', '000914.SH']
                 + list(wind_util.get_zz_size_index()['wind_code'])
                 + list(wind_util.get_qz_first_level_index()['wind_code'])
                 + list(wind_util.get_hs300_first_level_index()['wind_code'])
                 + list(wind_util.get_zz_hy_index()['wind_code'])
                 + list(wind_util.get_zz_cl_index()['wind_code'])
                 + list(wind_util.get_zz_zt_index()['wind_code'])
                 + list(wind_util.get_zz_hw_index()['wind_code'])
                 )
sec_pool_list = [x for x in sec_pool_list if not x.endswith('CSI')]
sec_pool_list = list(set(sec_pool_list))
df = wind_util.get_all_index()
sec_pool_list = wind_util.pack_sec_name(sec_pool_list, df)
stgy = shape_stgy.ShapeStgy(sec_pool_list, end_date, shape_period)
stgy.run()






