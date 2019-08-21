import datetime
import three_line_stgy
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
count = 0
for sec in sec_pool_list:
    stgy = three_line_stgy.ThreeLineStgy(sec, end_date, period_list=[10, 30, 60])
    stgy.show = False
    (latest_row, max_row, min_row) = stgy.run()
    if latest_row['shape'] in ('down_arrow', 'y_mirror_tick') and max_row['buy_profit'] > 0.5 and min_row['buy_profit'] > -0.5:
        count += 1
        print('[{0} {1}]'.format(sec[0], sec[1]))
        print('lastest: shape({0}), day({1})'.format(latest_row['shape'], latest_row.name))
        print('max: profit({0}), shape({1}), day({2})'.format(max_row['buy_profit'], max_row['shape'], max_row.name))
        print('min: profit({0}), shape({1}), day({2})'.format(min_row['buy_profit'], min_row['shape'], min_row.name))
print('--- total ({0}) ---'.format(count))








